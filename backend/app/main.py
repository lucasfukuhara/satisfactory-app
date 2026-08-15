from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models
from . import schemas

# Cria as tabelas automaticamente no banco ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Cadastro de Produtos")

@app.post("/produtos", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.ProdutoModel(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.ProdutoModel).all()