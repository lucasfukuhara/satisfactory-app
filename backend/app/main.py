from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import api_router  # Importa o centralizador unificado

# Cria as tabelas do banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Satisfactory App",
    version="1.0.0",
    description="API para cálculo recursivo de insumos e manufatura de itens de jogos."
)

# Configuração de segurança do CORS para conversar com o Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Injeta todas as rotas do sistema de uma só vez
app.include_router(api_router)

@app.get("/")
def check_health():
    return {"status": "online", "environment": "Meu PC"}