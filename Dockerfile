FROM python:3.13-slim AS base

WORKDIR /app

COPY pyproject.toml setup.py
COPY . /app/

RUN pip install .

CMD ["python3", "main.py"]
