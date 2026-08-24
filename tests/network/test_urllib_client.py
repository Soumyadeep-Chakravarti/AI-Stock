import threading
from collections.abc import Generator
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import ClassVar, override
from urllib.parse import parse_qs, urlsplit

import pytest

from ai_stock.network.errors import NetworkError
from ai_stock.network.types import HttpMethod, HttpRequest
from ai_stock.network.urllib_client import UrllibNetworkClient


class _TestHandler(BaseHTTPRequestHandler):
    received_method: ClassVar[str | None] = None
    received_body: ClassVar[bytes | None] = None
    received_query: ClassVar[dict[str, list[str]] | None] = None

    def do_GET(self) -> None:
        parts = urlsplit(self.path)

        if parts.path == "/test":
            body = b"hello"

            self.__class__.received_method = self.command
            self.__class__.received_query = parse_qs(
                parts.query,
                keep_blank_values=True,
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parts.path == "/error":
            body = b"bad request"

            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/test":
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        self.__class__.received_method = self.command
        self.__class__.received_body = body

        response_body = b"created"

        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.send_header(
            "Content-Length",
            str(len(response_body)),
        )
        self.end_headers()
        self.wfile.write(response_body)

    @override
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture
def base_url() -> Generator[str]:
    server = HTTPServer(
        ("127.0.0.1", 0),
        _TestHandler,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_get_request(base_url: str) -> None:
    client = UrllibNetworkClient()

    response = client.request(
        HttpRequest(
            method=HttpMethod.GET,
            url=f"{base_url}/test",
        )
    )

    assert response.status_code == 200
    assert response.body == b"hello"
    assert response.headers["Content-Type"] == "text/plain"


def test_query_parameters(base_url: str) -> None:
    client = UrllibNetworkClient()

    _ = client.request(
        HttpRequest(
            method=HttpMethod.GET,
            url=f"{base_url}/test",
            params={
                "symbol": "AAPL",
                "interval": "1d",
            },
        )
    )

    assert _TestHandler.received_query == {
        "symbol": ["AAPL"],
        "interval": ["1d"],
    }


def test_existing_query_parameters_are_preserved(
    base_url: str,
) -> None:
    client = UrllibNetworkClient()

    _ = client.request(
        HttpRequest(
            method=HttpMethod.GET,
            url=f"{base_url}/test?existing=value",
            params={"symbol": "AAPL"},
        )
    )

    assert _TestHandler.received_query == {
        "existing": ["value"],
        "symbol": ["AAPL"],
    }


def test_post_body_and_method(base_url: str) -> None:
    client = UrllibNetworkClient()

    response = client.request(
        HttpRequest(
            method=HttpMethod.POST,
            url=f"{base_url}/test",
            body=b'{"symbol":"AAPL"}',
        )
    )

    assert response.status_code == 201
    assert response.body == b"created"
    assert _TestHandler.received_method == "POST"
    assert _TestHandler.received_body == b'{"symbol":"AAPL"}'


def test_http_error_is_returned_as_response(
    base_url: str,
) -> None:
    client = UrllibNetworkClient()

    response = client.request(
        HttpRequest(
            method=HttpMethod.GET,
            url=f"{base_url}/error",
        )
    )

    assert response.status_code == 400
    assert response.body == b"bad request"


def test_transport_failure_raises_network_error() -> None:
    client = UrllibNetworkClient()

    with pytest.raises(NetworkError):
        _ = client.request(
            HttpRequest(
                method=HttpMethod.GET,
                url="http://127.0.0.1:1/",
            )
        )
