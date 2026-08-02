# Hotel Booking API

REST API for hotel booking: availability search by date range, concurrency-safe booking creation, JWT authentication.

Built with FastAPI, SQLAlchemy 2, PostgreSQL, and Alembic.

## Requirements

- [uv](https://docs.astral.sh/uv/#installation)
- Python 3.14, installed with `uv python install 3.14`
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Setup guide

```bash
uv sync                        # install dependencies
cp .env.example .env           # config — see below
docker compose up -d           # start PostgreSQL
uv run alembic upgrade head    # apply migrations
```

Generate a secret key and paste it into `JWT_KEY` in `.env`:

```bash
uv run python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Seed the database with demo data:

```bash
uv run python -m scripts.seed
```

Run the app:

```bash
uv run fastapi dev
```

Interactive docs: http://localhost:8000/docs

## Development

Format and lint:

```bash
uv run ruff format
uv run ruff check
```

Generate a migration from model changes, apply it, revert one revision, or roll everything back:

```bash
uv run alembic revision --autogenerate -m "msg"
uv run alembic upgrade head

uv run alembic downgrade -1
uv run alembic downgrade base
```

Check the database container, open a psql shell, or stop it and wipe the data:

```bash
docker compose exec db pg_isready
docker compose exec db psql -U postgres -d booking

docker compose down -v
```
