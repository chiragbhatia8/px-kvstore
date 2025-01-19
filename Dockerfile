FROM python:3.11-slim AS base

WORKDIR /app

COPY pyproject.toml setup.py /app/
COPY . /app/

RUN pip install .

CMD ["px-kvstore"]
