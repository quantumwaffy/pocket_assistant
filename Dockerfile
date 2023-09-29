FROM python:3.11-alpine


WORKDIR /app

RUN pip install poetry --root-user-action=ignore

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .
