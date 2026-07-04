# 🚀 Satisfactory App - Guia de Instalação e Execução

## 📋 Pré-requisitos

#### 1. Instalar Docker
#### 2. Instalar Docker Compose

---

## 🚀 Executando a Aplicação

### Opção 1: Com Docker Compose (Recomendado)

O Docker criará um ambiente isolado com o Python 3.14 compilando as dependências nativas e mantendo o banco SQLite persistido de forma segura na sua máquina física.

```bash
# 1. Clone o repositório e acesse a pasta raiz
cd satisfactory-app

# 2. Inicie os serviços em segundo plano (Background)
docker-compose up -d --build

```

**Acesse a aplicação:**
- **Frontend (Angular):** http://localhost:4200
- **Documentação da API (Swagger):** http://localhost:8000/docs
- **Health Check da API:** http://localhost:8000/

---

### Opção 2: Sem Docker (Instalação Local no Linux / Arch Linux)

Caso prefira rodar de forma nativa na sua máquina sem contêineres:

#### 🔩 Dependências do Sistema (Apenas se usar Arch Linux)
Antes de rodar o ambiente virtual, garanta que possui as ferramentas de compilação em C para o Python 3.14:
```bash
sudo pacman -S --needed base-devel
```

#### 🐍 Inicializando o Backend
```bash
# 1. Vá para o diretório backend
cd backend

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Atualizar os compiladores internos do ambiente
pip install --upgrade pip setuptools wheel

# 5. Instalar dependências atualizadas para o Python 3.14
pip install -r requirements.txt

# 6. OBRIGATÓRIO: Popular as tabelas do banco de dados local (jogo.db)
python seed.py

# 7. Executar a API usando o caminho do módulo estruturado
uvicorn app.main:app --reload
```

---

## 📝 Principais Comandos Docker Compose

Sempre execute estes comandos a partir da pasta onde o arquivo `docker-compose.yml` está localizado.

```bash
# Ver se o contêiner do jogo está ativo (Running)
docker compose ps

# Monitorar os logs e requisições HTTP da API em tempo real
docker compose logs -f api

# Parar a execução da aplicação
docker compose down

# Apagar a aplicação limpando volumes do banco de dados (Reseta o jogo)
docker compose down -v

# Forçar a reconstrução da imagem após mexer no requirements.txt
docker compose up -d --build
```

---

## 🎯 Guia de Testes Automatizados (Povoamento Inicial)

Graças ao script `seed.py` executado nos passos anteriores, sua árvore de dependências já vem pronta. Siga as etapas abaixo para validar o funcionamento do grafo recursivo:

1. **Verificar os Itens Cadastrados:**
   - Acesse o Swagger em `http://localhost:8000/docs`
   - Abra a rota `GET /api/itens/` e clique em *Execute*.
   - Note que o banco retornará a lista com IDs para **Minério de Ferro (ID 1)**, **Parafuso**, **Estator** e **Rotor (ID 9)**.

2. **Calcular o Custo Completo de Fabricação:**
   - Procure pela rota `GET /api/itens/calcular-plano`.
   - Clique em *Try it out*.
   - Preencha o parâmetro `item_id` com o número `9` (Rotor) e `quantidade` com `1`.
   - Clique em *Execute*.
   - **Resultado:** A API retornará um JSON estruturado detalhando que para 1 Rotor você precisa fazer exatamente 100 Parafusos, 20 Barras, 20 Lingotes e extrair 20 Minérios de Ferro, além dos componentes do Estator.

3. **Cadastrar Novos Itens Avançados via JSON:**
   Para adicionar novos componentes na malha do jogo, envie um payload para o `POST /api/itens/` informando os IDs das dependências:
   ```json
   {
     "nome": "Placa de Ferro Reforçada",
     "quantidade_estoque": 0,
     "receita_ingredientes": [
       {
         "item_ingrediente_id": 4,
         "quantidade_ingrediente": 6,
         "quantidade_produzida": 1
       },
       {
         "item_ingrediente_id": 5,
         "quantidade_ingrediente": 12,
         "quantidade_produzida": 1
       }
     ]
   }
   ```

---

## 🐛 Troubleshooting (Resolução de Problemas)

### Erro: `Bind for 0.0.0.0:8000 failed: port is already allocated`
Se o Docker acusar que a porta está presa mas o `lsof` retornar vazio, o kernel do Linux está com um proxy fantasma preso. Execute:

```bash
# Derruba redes órfãs e reinicia o daemon de rede do Docker no Arch
docker compose down --volumes --remove-orphans
sudo systemctl restart docker
docker compose up -d
```

### Erro: `TypeError: 'generator' object does not support the context manager protocol`
Esse erro acontece se o decorador `@contextmanager` for removido acidentalmente do topo da função `get_db()` dentro do arquivo `backend/app/database.py`. Garanta que a importação de `contextlib` está ativa e reinicie o contêiner:
```bash
docker compose restart api
```