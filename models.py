# models.py
from pydantic import BaseModel
from typing import Dict

# Pydantic usa le classi per definire la "forma" dei dati.
# Ereditando da BaseModel, otteniamo tutta la magia della validazione.
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