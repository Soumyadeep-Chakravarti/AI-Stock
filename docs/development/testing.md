# Testing

Run the full quality gate locally:

```bash
uv run ruff format .
uv run ruff check .
uv run basedpyright
uv run pytest -v
```

Pre-commit runs the same gate before each commit. Install it after syncing dependencies:

```bash
uv run pre-commit install
```

Run every configured hook manually with:

```bash
uv run pre-commit run --all-files
```

Test boundaries deliberately avoid live Albion dependencies:

- Network tests use a local HTTP server.
- Albion parser tests use static JSON fixtures.
- Albion client tests use a fake `NetworkClient`.
- Analysis tests use deterministic generic observations.
- Scanner tests use a fake current-price client.

Live Albion calls are experiments. A transient API failure, stale market, or missing quote must not make the unit suite fail.
