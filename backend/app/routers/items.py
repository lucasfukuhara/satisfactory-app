from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ItemJogo, ReceitaIngrediente
from app.schemas import (
    ItemJogoCreate, ItemJogoResponse, 
    RespostaPlanoProducao, ItemPlanoProducao
)

# O prefixo e a tag foram mantidos aqui para organizar a documentação automática (/docs)
router = APIRouter(prefix="/api/itens", tags=["Itens e Produção"])

def gerar_plano_recursivo(item_id: int, quantidade_necessaria: float, db: Session, plano_acumulado: dict):
    """Varre a árvore de receitas acumulando e somando subcomponentes e insumos brutos"""
    receitas = db.query(ReceitaIngrediente).filter_by(item_resultado_id=item_id).all()
    
    if not receitas:
        if item_id not in plano_acumulado:
            item = db.query(ItemJogo).filter_by(id=item_id).first()
            plano_acumulado[item_id] = {"nome": item.nome, "quantidade": 0, "eh_materia_prima": True}
        plano_acumulado[item_id]["quantidade"] += quantidade_necessaria
        return

    for receita in receitas:
        execucoes = (quantidade_necessaria / receita.quantidade_produzida)
        qtd_ingrediente = execucoes * receita.quantidade_ingrediente
        
        ingrediente = db.query(ItemJogo).filter_by(id=receita.item_ingrediente_id).first()
        
        if receita.item_ingrediente_id not in plano_acumulado:
            tem_sub_receita = db.query(ReceitaIngrediente).filter_by(item_resultado_id=receita.item_ingrediente_id).first()
            plano_acumulado[receita.item_ingrediente_id] = {
                "nome": ingrediente.nome,
                "quantidade": 0,
                "eh_materia_prima": tem_sub_receita is None
            }
            
        plano_acumulado[receita.item_ingrediente_id]["quantidade"] += qtd_ingrediente
        gerar_plano_recursivo(receita.item_ingrediente_id, qtd_ingrediente, db, plano_acumulado)


@router.get("/", response_model=List[ItemJogoResponse])
def listar_todos_itens():
    with get_db() as db:
        return db.query(ItemJogo).all()


@router.post("/", response_model=ItemJogoResponse, status_code=201)
def cadastrar_item_e_receita(item_in: ItemJogoCreate):
    with get_db() as db:
        item_existente = db.query(ItemJogo).filter_by(nome=item_in.nome).first()
        if item_existente:
            raise HTTPException(status_code=400, detail="Item com este nome já cadastrado.")

        novo_item = ItemJogo(nome=item_in.nome,
                             #quantidade_estoque=item_in.quantidade_estoque
                             )
        db.add(novo_item)
        db.flush()

        if item_in.receita_ingredientes:
            for ing in item_in.receita_ingredientes:
                ing_existe = db.query(ItemJogo).filter_by(id=ing.item_ingrediente_id).first()
                if not ing_existe:
                    raise HTTPException(status_code=404, detail=f"Ingrediente ID {ing.item_ingrediente_id} inválido.")
                
                vinculo = ReceitaIngrediente(
                    item_resultado_id=novo_item.id,
                    item_ingrediente_id=ing.item_ingrediente_id,
                    quantidade_ingrediente=ing.quantidade_ingrediente,
                    quantidade_produzida=ing.quantidade_produzida
                )
                db.add(vinculo)
        
        db.commit()
        db.refresh(novo_item)
        return novo_item


@router.get("/calcular-plano", response_model=RespostaPlanoProducao)
def calcular_plano_producao(item_id: int = Query(..., ge=1), quantidade: int = Query(..., ge=1)):
    with get_db() as db:
        item_alvo = db.query(ItemJogo).filter_by(id=item_id).first()
        if not item_alvo:
            raise HTTPException(status_code=404, detail="Item de destino não foi localizado.")
        
        plano_map = {}
        gerar_plano_recursivo(item_id, quantidade, db, plano_map)
        
        plano_final = [
            ItemPlanoProducao(
                item_id=id_item,
                nome=info["nome"],
                quantidade_necessaria=info["quantidade"],
                eh_materia_prima=info["eh_materia_prima"]
            )
            for id_item, info in plano_map.items()
        ]
        
        return RespostaPlanoProducao(
            item_alvo=item_alvo.nome,
            quantidade_solicitada=quantidade,
            plano_de_producao=plano_final
        )