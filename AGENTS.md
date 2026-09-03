# AGENTS.md

## Repository layout

- This is a Python 3.12+ library using the `src/` layout.
- Package code lives in `src/codescape/shared/`.
- Tests live in `tests/` and use pytest.
- Dependencies and tool configuration are defined in `pyproject.toml`; `uv.lock` is committed.

## Development commands

Use uv from the repository root:

- `uv sync --locked --dev`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy .`

The test command includes the configured coverage gate. Keep coverage focused on `codescape.shared`, and add or update tests with behavior changes.

## Change conventions

- Keep public APIs and the existing `src` layout stable unless the task requires otherwise.
- Use absolute imports from `codescape.shared`.
- Add explicit type annotations and keep changes narrowly scoped.
- Do not commit generated coverage reports, caches, virtual environments, or build artifacts.
