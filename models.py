from sqlalchemy import Column, Integer, String, JSON
from database import Base 

class Creation(Base):
    # Il nome della tabella nel database
    __tablename__ = 'creations'
    
    # Le nostre colonne
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)

    # SQLAlchemy ha un tipo JSON che mappa perfettamente
    # i nostri dizionari di parametri
    params = Column(JSON)