from fastapi import FastAPI, status, HTTPException

from typing import List

# Importiamo il nostro nuovo modello dal file models.py
from models import Creation, CreationCreate

# 1. Importa il middleware CORS
from fastapi.middleware.cors import CORSMiddleware

# Crea un'istanza dell'applicazione FastAPI
app = FastAPI()

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

# --- Finto Database ---
# In un'applicazione reale, questi dati proverrebbero da un database SQL o NoSQL.
# Per ora, usiamo una semplice lista in memoria per simulare i dati.
db_creations = [
    Creation(id=1, name="Spirale Cosmica", author="Mario", params={"color": "#FFFFFF", "speed": 0.8}),
    Creation(id=2, name="Pioggia di Meteore", author="Giulia", params={"color": "#00FF00", "count": 50}),
    Creation(id=3, name="Onde Sonore", author="Mario", params={"color": "#FF5733", "frequency": 12}),
]
# --------------------

# Definisce un endpoint per la radice ("/") che risponde alle richieste GET
@app.get("/")
def read_root():
    return {"message": "Hello from Generative Art API"}

# Qui definiamo il nostro nuovo endpoint
@app.get("/api/creations", response_model=List[Creation])
def get_creations():
    """
    Restituisce la lista di tutte le creazioni artistiche.
    """
    return db_creations

@app.post("/api/creations", response_model=Creation, status_code=status.HTTP_201_CREATED)
def create_creation(creation_data: CreationCreate):
    """
    Crea una nuova opera d'arte e la aggiunge al database (finto).
    """
    # 1. Calcola il nuovo ID (in un DB reale, questo è automatico)
    new_id = max(c.id for c in db_creations) + 1 if db_creations else 1

    # 2. Crea un oggetto Creation completo, unendo l'ID generato ai dati ricevuti
    new_creation = Creation(id=new_id, **creation_data.model_dump())

    # 3. Aggiungi il nuovo oggetto alla nostra lista in memoria
    db_creations.append(new_creation)

    # 4. Restituisci l'oggetto appena creato
    return new_creation

@app.delete("/api/creations/{creation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_creation(creation_id: int):
    """
    Trova una creazione tramite il suo ID e la elimina dal database (finto).
    """
    # Cerca nella nostra lista la creazione con l'ID corrispondente.
    # `next` si ferma al primo risultato trovato.
    creation_to_delete = next((c for c in db_creations if c.id == creation_id), None)

    # Se 'next' non trova nulla, restituisce None. In questo caso...
    if creation_to_delete is None:
        # ...solleviamo un'eccezione HTTP che FastAPI convertirà in una risposta 404.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Creation with id {creation_id} not found")

    # Se l'abbiamo trovata, la rimuoviamo dalla lista.
    db_creations.remove(creation_to_delete)

    # Restituiamo una risposta vuota con status code 204.
    return

@app.put("/api/creations/{creation_id}", response_model=Creation)
def update_creation(creation_id: int, creation_data: CreationCreate):
    """
    Trova una creazione tramite ID e aggiorna i suoi dati con quelli forniti.
    """
    # 1. Trova l'indice della creazione da aggiornare.
    # Usiamo l'indice invece dell'oggetto per poterlo poi sostituire nella lista.
    index_to_update = next((i for i, c in enumerate(db_creations) if c.id == creation_id), None)

    # 2. Se l'indice non viene trovato, solleva un errore 404.
    if index_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Creation with id {creation_id} not found")

    # 3. Crea un nuovo oggetto Creation con i dati aggiornati.
    # Manteniamo l'ID originale e usiamo i nuovi dati dal body della richiesta.
    updated_creation = Creation(id=creation_id, **creation_data.model_dump())

    # 4. Sostituisci il vecchio oggetto nella lista con quello nuovo.
    db_creations[index_to_update] = updated_creation

    # 5. Restituisci l'oggetto aggiornato.
    return updated_creation
