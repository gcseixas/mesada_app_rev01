# Mesada+

Aplicação Flask para controle de tarefas, aprovações e saldo de mesada entre pais e filhos.

## Requisitos

- Python 3.14
- Ambiente virtual `.venv`
- Banco PostgreSQL

## Configuração

1. Crie e ative o ambiente virtual.
2. Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Configure o arquivo `.env` com a conexão do banco:

```env
DATABASE_URL=postgresql://usuario:senha@host/database?sslmode=require
```

Observação:
A aplicação converte automaticamente `postgresql://` para `postgresql+psycopg://`.

## Executar a aplicação

```powershell
.\.venv\Scripts\python.exe run.py
```

Por padrão, a aplicação sobe em `http://127.0.0.1:5000`.

## Banco de dados e migrations

O projeto usa `Flask-Migrate` com Alembic.

Para aplicar as migrations pendentes:

```powershell
.\.venv\Scripts\flask.exe --app run.py db upgrade
```

Também é possível usar o atalho abaixo:

```powershell
.\.venv\Scripts\python.exe create_db.py
```

## Deploy no Render

O projeto já está preparado para subir no Render com o arquivo `render.yaml`.

Variáveis esperadas no ambiente:

- `DATABASE_URL`
- `SECRET_KEY`

Comandos usados no Render:

- build: `pip install -r requirements.txt`
- pre-deploy: `flask --app run.py db upgrade`
- start: `gunicorn run:app`

## Criar uma nova migration

Depois de alterar os models:

```powershell
.\.venv\Scripts\flask.exe --app run.py db migrate -m "descricao da alteracao"
```

Em seguida, aplique:

```powershell
.\.venv\Scripts\flask.exe --app run.py db upgrade
```

## Estrutura principal

- `app/__init__.py`: configuração da aplicação, SQLAlchemy, login e migrations
- `app/models.py`: models do banco
- `app/routes/`: rotas do sistema
- `app/templates/`: templates HTML
- `app/static/`: CSS e JavaScript
- `migrations/`: histórico de migrations do banco

## Fluxo atual do sistema

- Pai cria tarefas
- Filho lança tarefa para aprovação
- Pai aprova ou reprova
- Quando aprovada, a tarefa gera transação para o filho
- Quando reprovada, o motivo fica salvo no histórico
