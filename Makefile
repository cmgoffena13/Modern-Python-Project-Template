ready: format lint type-check test

format: 
	uv run -- ruff format

lint:
	uv run -- ruff check --fix

type-check:
	uv run -- ty check

test:
	uv run -- pytest -v -n auto

install:
	uv sync --all-extras
	uv run -- prek install

upgrade:
	uv sync --upgrade --all-extras

run:
	uv run main.py