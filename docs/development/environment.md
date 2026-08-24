# Development Environment

AI-Stock requires Python 3.14+ and uses `uv` for dependency and environment management.

```bash
uv sync
```

The repository includes a Nix development shell and direnv configuration. With Nix and direnv available:

```bash
direnv allow
```

The Nix shell provides Python, `uv`, Git/GitHub tools, `just`, pre-commit, code-search and HTTP utilities, SQLite, Nix/shell/YAML linters and formatters, secret scanning, spelling checks, and dependency auditing. Project Python dependencies remain managed through `uv` and the committed `uv.lock` file.

Use `just` to discover or run the supported development commands:

```bash
just
just check
just format
just coverage
just audit
```

`just check` runs linting, type checks, tests, and `nix flake check`. Run `just pre-commit` to execute the commit hooks manually.

The installed placeholder command is `ai-stock`. Application-facing commands should be added only when there is a stable use case beyond ad hoc live experiments.
