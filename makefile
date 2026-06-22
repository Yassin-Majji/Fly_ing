PYTHON = python3
MAIN = main.py
FILE = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

run:
	$(PYTHON) $(MAIN) $(FILE)

install:
	pip install pydantic flake8 mypy
# Run the main script in debug mode using python's built-in debugger
debug:
	$(PYTHON) -m pdb $(MAIN)

# Remove temporary files and caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Execute strict linting (optional but highly recommended)
lint-strict:
	flake8 .
	mypy . --strict