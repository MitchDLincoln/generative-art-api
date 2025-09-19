# models.py
from pydantic import BaseModel
from typing import Dict


# Questo modello definisce i dati necessari per CREARE una Creation.
# Nota l'assenza del campo 'id'.
class CreationCreate(BaseModel):
    name: str
    author: str
    params: Dict

# Pydantic usa le classi per definire la "forma" dei dati.
# Ereditando da BaseModel, otteniamo tutta la magia della validazione.
# Questo modello rappresenta i dati che RESTITUIAMO al client.
# Contiene tutti i campi, incluso l'id generato dal server.
class Creation(BaseModel):
    """
    Rappresenta una singola creazione artistica generativa.
    """
    id: int
    name: str
    author: str
    # 'params' conterrà le impostazioni dell'animazione,
    # ad esempio: {"color": "#FF0000", "particleCount": 100}.
    # Usiamo 'Dict' per indicare un dizionario (oggetto JSON).
    params: Dict