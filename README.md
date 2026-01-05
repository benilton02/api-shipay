# shipay-api

Este projeto é uma API desenvolvida com **FastAPI** seguindo os princípios da **Clean Architecture**. A aplicação utiliza **SQLAlchemy** como ORM para interação com banco de dados SQLite, **Alembic** para migrações de banco de dados e **pytest** para testes unitários. O gerenciamento de dependências é feito com **uv** para garantir um ambiente de desenvolvimento consistente e eficiente.

**Tecnologias principais:**
- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **Clean Architecture**: Organização do código em camadas (dtos, use cases, repositories, controllers etc.)
- **SQLAlchemy**: ORM para interação com banco de dados
- **Alembic**: Ferramenta para migrações de banco de dados
- **pytest**: Framework para testes unitários e de integração
- **uv**: Gerenciador de pacotes e ambientes virtuais de alta performance

## Endpoints da API

A API conta com os seguintes endpoints:

1. **POST /users** - Criação de usuários
   - Recebe dados do usuário (nome, email, senha, role_id)
   - Valida os dados e salva no banco de dados
   - Retorna os dados do usuário criado

2. **GET /users?email={email}** - Busca usuário por email
   - Recebe um email como parâmetro
   - Busca o usuário correspondente no banco de dados
   - Retorna os dados do usuário encontrado

## Seed de Dados

Durante a execução das migrações do Alembic, é executada uma **seed** que cria um usuário inicial no banco de dados. Este usuário de exemplo facilita o desenvolvimento e testes da aplicação. A seed está na migração **2026_01_04_1601-7d0ceb273b23_create_users_table.py**

**Usuário padrão criado na seed:**
```json
{
  "content": {
    "id": 1,
    "name": "first_user",
    "email": "user@example.com",
    "role_id": 1,
    "created_at": "2026-01-05T04:10:55.796619",
    "updated_at": null,
    "claims": [
      {
        "id": 1,
        "description": "can_create_users",
        "active": true
      },
      {
        "id": 2,
        "description": "can_delete_users",
        "active": false
      }
    ]
  }
}
```

## 1. Instalar o uv

Instale o **uv** usando o pip e verifique a versão instalada:

```bash
pip install uv
uv --version
```

## 2. Criar virtual env

```bash
uv venv
```

## 3. Ativar virtual env

```bash
source .venv/bin/activate
```

## 4. Instalar dependências de desenvolvimento e testes

```bash
uv sync
```

## 5. Configurar variáveis de ambiente

Antes de executar a aplicação, é necessário criar um arquivo `.env` na raiz do projeto para configurar a conexão com o banco de dados SQLite. Crie o arquivo com a seguinte variável:

```
DATABASE_URL=sqlite:///./app.db
```

Use o arquivo `.env-dev` como referência para outras configurações de ambiente necessárias.

## 6. Configurar banco de dados com Alembic

Para criar e atualizar as tabelas do banco de dados, execute o comando de migração do Alembic:

```bash
alembic upgrade heads
```

Este comando aplicará todas as migrações pendentes, criará a estrutura do banco de dados conforme definido nos modelos SQLAlchemy e executará a seed que cria um usuário inicial com os dados acima.

## 7. Executar a aplicação

Para executar a aplicação FastAPI, utilize o seguinte comando na raiz do projeto:

```bash
fastapi run
```

A API estará disponível em `http://localhost:8000`. A documentação interativa da API (Swagger UI) estará disponível em `http://localhost:8000/docs`.

## 8. Executar testes unitários

Para executar os testes unitários, utilize o seguinte comando na raiz do projeto:

```bash
pytest
```