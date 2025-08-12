# https://just.systems

export PYTHONPATH := "src"
HOST := "0.0.0.0"
PORT := "8000"

ARGS_TEST := env("_UV_RUN_ARGS_TEST", "")

@_:
   just --list

# Run the application
[group('run')]
run:
    uv run uvicorn assistant.asgi:app --reload --host {{ HOST }} --port {{ PORT }}

# Update dependencies
[group('lifecycle')]
update:
    uv sync --upgrade

# Ensure project virtualenv is up to date
[group('lifecycle')]
install:
    uv sync --group dev

# Remove temporary files
[group('lifecycle')]
clean:
    rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
    find . -type d -name "__pycache__" -exec rm -r {} +

# Remove uploaded files
[group('lifecycle')]
clean-instance:
    rm -rf .instance || true

# Remove temporary files, incl. virtualenv
[group('lifecycle')]
clean-all: clean clean-instance
    rm -rf .venv || true

# Recreate project virtualenv from nothing
[group('lifecycle')]
fresh: clean-all install

# Run pylint for errors only
[group('qa')]
pylint:
    @echo "Running pylint... It will take a while."
    @uv pip install pylint
    uv run pylint .

# Run linters and formatters
[group('qa')]
lint:
    uvx ruff format src tests
    uvx black src tests
    uvx ruff check src tests --fix --unsafe-fixes

# Run tests
[group('qa')]
test *args:
    uv run {{ ARGS_TEST }} -m pytest {{ args }}

_cov *args:
    uv run -m coverage {{ args }}

# Run tests and measure coverage
[group('qa')]
@cov:
    just _cov erase
    just _cov run -m pytest tests
    just _cov report

# Check types
[group('qa')]
typing:
    uvx ty check --python .venv src

# Perform all checks
[group('qa')]
check-all: lint cov typing

# Run pre-commit hooks
[group('qa')]
pre-commit:
    pre-commit run --all-files

# vim: set filetype=Makefile ts=4 sw=4 et:
