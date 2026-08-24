#!/usr/bin/bash
set -e

ruff format --check
ruff check --preview --extend-select PLR --output-format=full src
pytest --cov=. --cov-report=term-missing

for i in all_boundingboxes.sh all_adjust_viewboxes.sh all_path_options.sh all_strats.sh
do
  examples/$i
done

