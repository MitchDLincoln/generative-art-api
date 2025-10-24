# models.py
from pydantic import BaseModel
from typing import Dict


# Questo è il modello di "base", senza campi specifici del DB
class CreationBase(BaseModel):
    name: str
    author: str
    params: Dict

# Questo è usato per la CREAZIONE (non si passa un id)
class CreationCreate(CreationBase):
    pass

# Questo è il modello per la LETTURA (include l'id)
class Creation(CreationBase):
    id: int

    # Questa configurazione dice a Pydantic
    # di leggere i dati anche se sono un modello ORM (SQLAlchemy)
    class Config:
        from_attributes = True