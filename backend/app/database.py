from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from contextlib import contextmanager 

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    autocommit= False, 
    autoflush= False, 
    bind=engine
)

Base = declarative_base()

# Função que garante que a conexão fecha após a requisição terminar
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()