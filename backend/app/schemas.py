from pydantic import BaseModel
from typing import Optional

# 1. Base Schema: Campos comuns a todas as operações
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

# 2. Schema de Criação (Input DTO): Usado nas requisições POST/PUT
# Herda da base. Se precisar de validações extras específicas da criação, entram aqui.
class ProdutoResponse(ProdutoCreate):
    id: int

    # Permite que o Pydantic converta objetos do SQLAlchemy (ORM) diretamente em JSON
    class Config:
        from_attributes = True