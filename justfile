# Format project code
format:
    uv run ruff format

# Check project code for type and linting errors, auto-fix if possible
lint:
    uv run ruff check --fix
    uv run ty check

# Run automated tests
test:
    uv run pytest --verbose --color=yes tests

# Format, lint, and test project
validate: format lint test
