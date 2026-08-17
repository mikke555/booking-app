FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

ENV UV_PYTHON_DOWNLOADS=0
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

FROM python:3.14-slim

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["fastapi", "run"]
