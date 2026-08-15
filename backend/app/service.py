from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, schemas

# O schema serve como um DTO
def salva_item(item: schemas.ProdutoCreate, db: Session) -> models.ProdutoModel:
    if item.preco <= 0 :
        raise ValueError("O preço não pode ser zero!")

    db_item = models.ProdutoModel(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
