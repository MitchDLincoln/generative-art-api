from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Definiamo l'URL del nostro database.
# "sqlite:///./generative_art.db" significa che useremo un file SQLite
# chiamato 'generative_art.db' nella stessa cartella.
DATABASE_URL = "sqlite:///./generative_art.db"

engine = create_engine(
    DATABASE_URL, 

    # Questo è necessario solo per SQLite per permettere la connessione
    # da più thread (come fa FastAPI)
    connect_args={"check_same_thread": False}
    ) 

# 3. Creiamo una "fabbrica" di sessioni
# La Sessione sarà la nostra connessione individuale al DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creiamo una classe Base
# I nostri modelli di tabella del DB erediteranno da questa classe
Base = declarative_base()