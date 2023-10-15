#!/bin/sh -e
set -x

poetry run ruff --fix src
poetry run black src