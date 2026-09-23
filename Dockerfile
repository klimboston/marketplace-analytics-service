FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
COPY README.md ./

ENV PYTHONPATH=.

CMD ["uv", "run", "uvicorn", "src.marketplace_analytics_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
