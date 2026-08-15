from pydantic import BaseModel
from typing import Optional

class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

class ProdutoResponse(ProdutoCreate):
    id: int

    class Config:
        from_attributes = True