from fastapi import FastAPI
from typing import List

# Importiamo il nostro nuovo modello dal file models.py
from models import Creation

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