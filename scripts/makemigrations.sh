#!/bin/sh -e

poetry run alembic revision -m "$1" --autogenerate