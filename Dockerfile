FROM python:3.11.5
RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .
RUN poetry install --only-root

ENV PATH "$PATH:/scripts"

CMD poetry run python newsletter_backend
