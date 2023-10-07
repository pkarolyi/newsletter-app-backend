FROM python:3.11.5-slim-bullseye
RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .
RUN poetry install --only-root

CMD poetry run python newsletter_backend
