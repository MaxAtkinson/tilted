.PHONY: format_all
format_all: sort_imports format lint check_types

.PHONY: lint_all
lint_all: check_imports check_format check_types lint

.PHONY: format
format:
	poetry run black .

.PHONY: check_format
check_format:
	poetry run black --diff --check .

.PHONY: lint
lint:
	poetry run flake8 .

.PHONY: check_types
check_types:
	poetry run mypy . --no-incremental

.PHONY: check_types_incremental
check_types_incremental:
	poetry run mypy .

.PHONY: sort_imports
sort_imports:
	poetry run isort .

.PHONY: check_imports
check_imports:
	poetry run isort --check-only --diff .

.PHONY: coverage
coverage:
	{ \
		pytest --cov=tilted --cov-config=setup.cfg --cov-report=html --cov-report=term ;\
	}
