# Hotel Booking API

[![CI](https://github.com/mikke555/booking-app/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/mikke555/booking-app/actions/workflows/ci.yml)

REST API for hotel booking: availability search by date range, concurrency-safe booking creation, JWT authentication.

Built with FastAPI, SQLAlchemy 2, PostgreSQL, and Alembic.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- For running locally: [uv](https://docs.astral.sh/uv/#installation) and Python 3.14, installed with `uv python install 3.14`

## Configuration

```bash
cp .env.example .env
```

Generate a secret key and paste it into `JWT_KEY` in `.env`:

```bash
uv run python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Run with Docker

```bash
docker compose up -d
```

This builds the app image, starts PostgreSQL, applies migrations, and serves the API.

Seed the database with demo data (optional):

```bash
docker compose run --rm app python -m scripts.seed
```

Rebuild the app image after code or dependency changes:

```bash
docker compose up -d --build
```

## Run locally

```bash
uv sync                        # install dependencies
docker compose up -d db        # start PostgreSQL only
uv run alembic upgrade head    # apply migrations
uv run python -m scripts.seed  # seed demo data (optional)
uv run fastapi dev             # run with auto-reload
```

## Testing

Tests run against a separate `booking_test` database, configured via `.env.test`. The database is created automatically by an init script in `docker/initdb/` when the Postgres data volume is first initialized.

Run the tests:

```bash
uv run pytest
```

Run the tests under coverage, then print the report:

```bash
uv run coverage run -m pytest
uv run coverage report
uv run coverage html    # htmlcov/index.html
```

## Development

Format, lint, and type-check:

```bash
uv run ruff format
uv run ruff check
uv run pyright
```

Generate a migration from model changes, apply it, revert one revision, or roll everything back:

```bash
uv run alembic revision --autogenerate -m "msg"
uv run alembic upgrade head

uv run alembic downgrade -1
uv run alembic downgrade base
```

Check the database container, open a psql shell, or stop everything and wipe the data:

```bash
docker compose exec db pg_isready
docker compose exec db psql -U postgres -d booking

docker compose down -v
```
