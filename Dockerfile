FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    EDGE_BACKEND_ENVIRONMENT=production \
    EDGE_BACKEND_VERSION=0.1.0-beta \
    EDGE_PROTOCOL_VERSION=1.0.0 \
    MIN_EDGE_CLIENT_VERSION=0.2.2-3

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app

RUN pip install --no-cache-dir .

EXPOSE 8010

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
