# FastAPI-starter

A FastAPI starter template with SQLAlchemy, Alembic migrations, and a PostgreSQL database running in Docker.

## Requirements

- Install [UV](https://docs.astral.sh/uv/#installation)
- Python 3.14, installed with `uv python install 3.14`
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Setup guide

```bash
uv sync
mv .env.example .env
docker compose up -d
```

Create your own models in `./app/models`, then migrate:

```bash
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
```

Finally, run the app with UV:

```bash
uv run fastapi dev
```

## Reference / cheatsheet

### Docker

Start the PostgreSQL container in detached mode:

```bash
docker compose up -d
```

Check connection:

```bash
docker compose exec postgres pg_isready
```

Stop and remove the container, including volumes:

```bash
docker compose down -v
```

### Alembic

Create Alembic migration environment with async template (one-time setup, already done):

```bash
uv run alembic init -t async migrations
```

Generate a migration from model changes, then apply it:

```bash
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
```

Go down one revision:

```bash
uv run alembic downgrade -1
```

Downgrade back to nothing:

```bash
uv run alembic downgrade base
```

### Ruff

Autofix formatting & check for linting errors:

```bash
uv run ruff format
uv run ruff check
```
