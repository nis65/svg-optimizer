#!/usr/bin/bash
set -e

ruff check --preview --extend-select PLR --output-format=full src
pytest --cov=. --cov-report=term-missing

# todo: run test scripts in example directory
