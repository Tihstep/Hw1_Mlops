FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "mlops.fastapi_app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]

