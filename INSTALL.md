# Guia de Instalação e Execução

Este documento contém as instruções necessárias para instalar, configurar, monitorar e executar a aplicação backend (**FastAPI + PostgreSQL**) utilizando **Docker Compose**.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas em seu ambiente:

* [Docker](https://docs.docker.com/get-docker/) (versão 20.10 ou superior)
* [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0 ou superior)

---

## 🚀 Executando a Aplicação com Docker Compose

Todas as instruções e serviços (API Python e Banco de Dados PostgreSQL) estão orquestrados no arquivo `docker-compose.yml`.

### 1. Subir os Containers

Navegue até o diretório `backend` do projeto e execute o comando abaixo para construir as imagens e iniciar os serviços em segundo plano (*detached mode*):

```bash
docker compose up -d --build
```

---

## 🔍 Monitoramento e Verificação (Processos e Logs)

### 2. Verificar os Processos dos Containers

Para listar todos os containers ativos no projeto e verificar o status da aplicação e do banco de dados:

```bash
docker ps
```

Se quiser verificar todos os containers (inclusive os parados ou que falharam na inicialização):

```bash
docker ps -a
```

### 3. Verificar os Logs da Aplicação

Para acompanhar os logs em tempo real do container da API (`satisfactory_app`):

```bash
docker logs -f satisfactory_app
```

Para visualizar apenas as últimas 50 linhas do log:

```bash
docker logs --tail 50 satisfactory_app
```

Para verificar os logs do banco de dados PostgreSQL (`postgres_db`):

```bash
docker logs -f postgres_db
```

---

## 🌐 Acessando a API e Documentação

Com os containers em execução, acesse a documentação e os endpoints através das URLs abaixo:

* **Documentação Interativa (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Documentação Alternativa (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Endpoint de Cadastro e Listagem de Produtos:** `http://localhost:8000/produtos`

---

## ⚠️ Solução de Problemas: Atualizando de uma Versão Antiga da Aplicação

Se você já executou versões anteriores do projeto na mesma máquina ou alterou configurações do banco de dados (como nome do banco, tabelas ou variáveis de ambiente), o Docker pode manter volumes e caches antigos armazenados.

Para limpar completamente o ambiente antigo e forçar a recriação limpa de todos os serviços, siga os passos abaixo:

### Passo 1: Parar os containers e remover volumes/órfãos

O comando abaixo encerra os containers em execução, remove os volumes persistentes do PostgreSQL (garantindo que scripts de inicialização do banco sejam reexecutados) e remove containers órfãos de builds anteriores:

```bash
docker compose down -v --remove-orphans
```

### Passo 2: Reconstruir as imagens sem cache e recriar os containers

Em seguida, force a reconstrução completa das imagens Docker a partir do `Dockerfile` atual e reinicie os containers:

```bash
docker compose up -d --build --force-recreate
```

### Passo 3: Confirmar a inicialização

Acompanhe os logs para validar que a nova versão subiu com sucesso:

```bash
docker logs -f satisfactory_app
```

Você deverá visualizar a mensagem `INFO: Application startup complete.` indicando que a aplicação está pronta para uso.