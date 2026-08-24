from typing import Protocol

from ai_stock.network.types import HttpRequest, HttpResponse


class NetworkClient(Protocol):
    def request(self, request: HttpRequest) -> HttpResponse: ...
