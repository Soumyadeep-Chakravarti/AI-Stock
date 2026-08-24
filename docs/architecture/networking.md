# Networking

The network layer provides a small HTTP transport boundary:

```text
HttpRequest -> NetworkClient -> UrllibNetworkClient -> HttpResponse
```

`HttpRequest` carries method, URL, headers, parameters, and an optional byte body. `HttpResponse` carries status, headers, and raw bytes.

`NetworkClient` is a protocol so providers can depend on transport behavior without depending on `urllib`. The current `UrllibNetworkClient`:

- Preserves existing URL query parameters.
- Adds request query parameters.
- Returns HTTP 4xx/5xx responses normally for provider handling.
- Raises `NetworkError` for transport failures.
- Closes raw responses after reading them.

The network layer does not parse JSON and does not understand market data.
