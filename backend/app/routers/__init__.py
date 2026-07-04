from fastapi import APIRouter
from app.routers import items

# Criamos o roteador principal da API
api_router = APIRouter()

# Incluímos o roteador de itens. 
api_router.include_router(items.router)