# Backend - Satisfactory APP API

API REST desenvolvida com FastAPI para gerenciar recursos e receitas.

## Instalação

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Executar

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

## Endpoints

- `GET /materials` - Listar materiais
- `POST /materials` - Criar material
- `GET /recipes` - Listar receitas
- `POST /recipes` - Criar receita
- `POST /recipes/{id}/calculate` - Calcular recursos necessários