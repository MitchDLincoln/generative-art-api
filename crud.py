from sqlalchemy.orm import Session
import models, schemas

def get_creation(db: Session, creation_id: int): 
    # Interroga il DB per il modello Creation con l'id specificato
    return db.query(models.Creation).filter(models.Creation.id == creation_id).first()

def get_creations(db: Session, skip: int = 0, limit: int = 100):
    # Interroga per tutti, con paginazione
    return db.query(models.Creation).offset(skip).limit(limit).all()

def create_creation(db:Session, creation: schemas.CreationCreate):
    # 1. Converte il modello Pydantic (schema) in un dizionario
    db_data_creation = creation.model_dump()

    # 2. Crea un modello SQLAlchemy (ORM)
    db_creation = models.Creation(**db_data_creation)
    
    # 3. Aggiunge, fa il commit e aggiorna
    db.add(db_creation)
    db.commit()
    db.refresh(db_creation)

    return db_creation

def update_creation(db:Session, creation_id: int, creation: schemas.CreationCreate):
    db_creation = get_creation(db, creation_id)

    if not db_creation:
        return None
    
    update_data = creation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_creation, key, value)

    db.commit()
    db.refresh(db_creation)
    return db_creation

def delete_creation(db: Session, creation_id: int):
    db_creation = get_creation(db, creation_id)

    if not db_creation:
        return None
    
    db.delete(db_creation)
    db.commit()
    return db_creation
