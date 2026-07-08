from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# --- Schemas de Criação e Retorno Base de Itens ---
class IngredienteVinculo(BaseModel):
    item_ingrediente: str = Field(..., min_length=2, max_length=99)
    quantidade_ingrediente: float
    quantidade_produzida: float

class ItemJogoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=99)
    # quantidade_estoque: int = Field(default=0, ge=0)
    # Permite passar os ingredientes diretamente ao criar o item
    receita_ingredientes: Optional[List[IngredienteVinculo]] = []

class ItemJogoResponse(BaseModel):
    id: int
    nome: str
    # quantidade_estoque: int

    model_config = ConfigDict(from_attributes=True)

# --- Schemas do Plano de Produção ---
class ItemPlanoProducao(BaseModel):
    item_id: int
    nome: str
    quantidade_necessaria: float
    eh_materia_prima: bool

class RespostaPlanoProducao(BaseModel):
    item_alvo: str
    quantidade_solicitada: float
    plano_de_producao: List[ItemPlanoProducao]