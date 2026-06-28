PYTHON = python3
MAIN = main.py
FILE = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

run:
	$(PYTHON) $(MAIN) $(FILE)

install:
	pip install pydantic flake8 mypy
debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict