from fastapi import FastAPI, status, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import List

from contextlib import asynccontextmanager

# Importiamo i nostri nuovi file
import models, schemas, crud, database
from database import SessionLocal, engine

# Import per la sessione DB
from sqlalchemy.orm import Session

# --- Creazione Tabelle ---
# Questa riga dice a SQLAlchemy di creare tutte le tabelle
# definite in models.py (usando la Base) la prima volta
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager 
async def lifespan(app: FastAPI):
    # Codice da eseguire all'avvio
    models.Base.metadata.create_all(bind=engine)
    
    yield

# Crea un'istanza dell'applicazione FastAPI
app = FastAPI(lifespan=lifespan)

# 2. Definisci da quali "origini" (frontend) accetti le richieste
origins = [
    "http://localhost:4200",
]

# 3. Aggiungi il middleware alla tua applicazione
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permetti tutti i metodi (GET, POST, etc.)
    allow_headers=["*"], # Permetti tutti gli header
)

# --- Dependency per il Database ---
# Questa è la parte MAGICA.
# Questa funzione aprirà una sessione DB per ogni richiesta
# e si assicurerà di chiuderla alla fine (anche se c'è un errore).
def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


# Definisce un endpoint per la radice ("/") che risponde alle richieste GET
@app.get("/")
def read_root():
    return {"message": "Hello from Generative Art API"}

# Qui definiamo il nostro nuovo endpoint
@app.get("/api/creations", response_model=List[schemas.Creation])
def get_creations_endpoint(skip: int = 0, limit: int = 100, db : Session = Depends(get_db)):
    """
    Restituisce la lista di tutte le creazioni artistiche.
    """
    db_creations = crud.get_creations(db, skip=skip, limit=limit)

    return db_creations

@app.post("/api/creations", response_model=schemas.Creation, status_code=status.HTTP_201_CREATED)
def create_creation_endpoint(creation_data: schemas.CreationCreate, db : Session = Depends(get_db)):
    """
    Crea una nuova opera d'arte e la aggiunge al database (finto).
    """
    new_creation = crud.create_creation(db, creation=creation_data)
    return new_creation

@app.delete("/api/creations/{creation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_creation_endpoint(creation_id: int, db : Session =  Depends(get_db)):
    """
    Trova una creazione tramite il suo ID e la elimina dal database (finto).
    """
    # Cerca nella nostra lista la creazione con l'ID corrispondente.
    # `next` si ferma al primo risultato trovato.
    delete_creation = crud.delete_creation(db, creation_id=creation_id)

    # Se 'next' non trova nulla, restituisce None. In questo caso...
    if delete_creation is None:
        # ...solleviamo un'eccezione HTTP che FastAPI convertirà in una risposta 404.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Creation with id {creation_id} not found")


    return delete_creation

@app.put("/api/creations/{creation_id}", response_model=schemas.Creation)
def update_creation_endpoint(creation_id: int, creation_data: schemas.CreationCreate, db : Session =  Depends(get_db)):
    """
    Trova una creazione tramite ID e aggiorna i suoi dati con quelli forniti.
    """

    updated_creation = crud.update_creation(db, creation_id=creation_id, creation=creation_data)

    if updated_creation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Creation with id {creation_id} not found")

    return updated_creation
