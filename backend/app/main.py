from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models
from . import schemas
from . import service

# Cria as tabelas automaticamente no banco ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de modelo para o Satisfactory")


@app.post(
    "/produtos",
    response_model=schemas.ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        return service.salva_item(produto, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.ProdutoModel).all()
