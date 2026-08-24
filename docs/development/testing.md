# Testing

Run the full quality gate locally:

```bash
uv run ruff format .
uv run ruff check .
uv run basedpyright
uv run pytest -v
```

Test boundaries deliberately avoid live Albion dependencies:

- Network tests use a local HTTP server.
- Albion parser tests use static JSON fixtures.
- Albion client tests use a fake `NetworkClient`.
- Analysis tests use deterministic generic observations.
- Scanner tests use a fake current-price client.

Live Albion calls are experiments. A transient API failure, stale market, or missing quote must not make the unit suite fail.
