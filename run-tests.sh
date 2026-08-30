#!/usr/bin/bash
set -e

ruff format --check
ruff check --preview --extend-select PLR --output-format=full src
pytest --cov=. --cov-report=term-missing --cov-fail-under=100

for i in all_boundingboxes.sh all_path_options.sh all_strats.sh
do
  echo "=====================  running $i =========================="
  examples/$i
done

