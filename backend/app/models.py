from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ReceitaIngrediente(Base):
    """Tabela de associação que conecta um item aos seus ingredientes necessários"""
    __tablename__ = "receitasV2"

    item_resultado_id: Mapped[int] = mapped_column(
        ForeignKey("itens.id", ondelete="CASCADE"), primary_key=True
    )
    item_ingrediente_id: Mapped[int] = mapped_column(
        ForeignKey("itens.id", ondelete="CASCADE"), primary_key=True
    )

    quantidade_ingrediente: Mapped[float] = mapped_column(Float, default=1.0)
    quantidade_produzida: Mapped[float] = mapped_column(Float, default=1.0)


class ItemJogo(Base):
    """Tabela principal contendo insumos brutos, intermediários e produtos finais"""
    __tablename__ = "itens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    # quantidade_estoque: Mapped[int] = mapped_column(Integer, default=0)

    # # Relacionamento: O que este item precisa para ser fabricado (Lê a partir do resultado)
    # ingredientes: Mapped[List["ReceitaIngrediente"]] = relationship(
    #     foreign_keys=[ReceitaIngrediente.item_resultado_id],
    #     backref="produzido_por",
    #     cascade="all, delete-orphan"
    # )
    # 
    # # Relacionamento Reverso: Em quais receitas este item é usado como parte do processo
    # usado_em: Mapped[List["ReceitaIngrediente"]] = relationship(
    #     foreign_keys=[ReceitaIngrediente.item_ingrediente_id],
    #     backref="usado_como_ingrediente",
    #     cascade="all, delete-orphan"
    # )