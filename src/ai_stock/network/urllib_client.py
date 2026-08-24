from collections.abc import Iterator
from typing import Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from ai_stock.network.errors import NetworkError
from ai_stock.network.types import HttpRequest, HttpResponse


class _ResponseHeaders(Protocol):
    def items(self) -> Iterator[tuple[str, str]]: ...


class _UrlopenResponse(Protocol):
    status: int
    headers: _ResponseHeaders

    def read(self) -> bytes: ...

    def close(self) -> None: ...


class UrllibNetworkClient:
    def request(self, request: HttpRequest) -> HttpResponse:
        parts = urlsplit(request.url)
        existing_params = parse_qsl(parts.query, keep_blank_values=True)
        request_params = list(request.params.items())

        query = urlencode(
            existing_params + request_params,
        )

        url = urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                query,
                parts.fragment,
            )
        )

        http_request = Request(
            url=url,
            headers=dict(request.headers),
            data=request.body,
            method=request.method.value,
        )

        try:
            raw_response = cast(
                _UrlopenResponse,
                urlopen(http_request),
            )
        except HTTPError as error:
            return HttpResponse(
                status_code=error.code,
                headers=dict(error.headers.items()),
                body=error.read(),
            )
        except URLError as error:
            raise NetworkError(f"Network request failed: {error.reason}") from error

        try:
            body = raw_response.read()
            status_code = raw_response.status
            headers = dict(raw_response.headers.items())
        finally:
            raw_response.close()

        return HttpResponse(
            status_code=status_code,
            headers=headers,
            body=body,
        )
