# Development Environment

AI-Stock requires Python 3.14+ and uses `uv` for dependency and environment management.

```bash
uv sync
```

The repository includes a Nix development shell and direnv configuration. With Nix and direnv available:

```bash
direnv allow
```

The Nix shell provides Python and `uv`; project dependencies remain managed through `uv` and the committed `uv.lock` file.

The installed placeholder command is `ai-stock`. Application-facing commands should be added only when there is a stable use case beyond ad hoc live experiments.
