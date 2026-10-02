# Modern Python Project Template

Example Python Project showcasing best practices in configuration, logging, testing, and CI/CD.

## Development Tools
 - `uv`: manage python versions, package dependencies, and environments
 - `ruff`: format code & lint code to enforce best practices
 - `ty`: check type annotations, ensuring code is understandable
 - `pytest`: run tests to prevent regressions
 - `pytest-xdist`: run tests in parallel for speed improvements
 - `pytest-cov`: allow for test coverage reporting
 - `prek`: replacement of `pre-commit`; enforce formatting, linting, type-checking, and test runs on git commits
 - `Makefile`: alias and chain commands together for easy development
 - `pydantic`: validate data to ensure its in the correct format
 - `pydantic-settings`: replacement of `python-dotenv`; validate settings values to ensure correct configuration
 - `docker`: containerize code for reproducability and easy deployment
 - `git`: track changes of codebase utilizing source control
 - `structlog`: replacement of builtin `logging`; allows for key:value pairs to easily be logged
 - `opentelemetry`: de-facto logging standard format; send logs anywhere

## Optional Development Tools
 - `polars`: replacement of `pandas`; transform data quickly and efficiently
 - `httpx2`: replacement of `requests`; send requests quickly and securely
 - `sqlmodel`: replacement of `sqlalchemy` & `pydantic`; validate and mirror data/schemas against a database
 - `fastapi`: replacement of `flask`; modern web framework
 - `granian`: replacement of `gunicorn` / `uvicorn`; rust-based web server
 - `orjson`: replacement of builtin `json`; serialize/deserialize json at lightning speeds
 - `pendulum`: replacement of builtin `datetime`; easily work with times and dates
 - `eventsourcing`: Python event sourcing library; time-aware storage of data
 - `xxhash`: fast non-cryptographic hashing for data comparison
 - `typer`: easy & simple CLI setup; prefer `argparse` if speed is needed