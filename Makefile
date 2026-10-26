.PHONY: ready format lint type-check test test-cov install upgrade run clean reset

install:
	uv sync --all-extras
	uv run -- prek install
	cp .env.example .env

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -f .coverage

reset: clean
	uv venv --clear
	$(MAKE) install

upgrade:
	uv sync --upgrade --all-extras

ready: lint format type-check test-cov

format: 
	uv run -- ruff format

lint:
	uv run -- ruff check --fix

type-check:
	uv run -- ty check

test:
	uv run -- pytest -v -n auto

test-cov:
	uv run -- pytest -v -n auto --cov=src --cov-report=term-missing

run:
	uv run -- python -m src.main