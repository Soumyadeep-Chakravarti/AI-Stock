from collections.abc import Sequence

import pytest

from ai_stock.market.types import CurrentPriceObservation
from ai_stock.network.types import HttpRequest, HttpResponse
from ai_stock.providers.albion.client import AlbionApiError, AlbionCurrentPriceClient
from ai_stock.providers.albion.types import (
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class _FakeNetworkClient:
    def __init__(self, response: HttpResponse) -> None:
        self.response = response
        self.requests: list[HttpRequest] = []

    def request(self, request: HttpRequest) -> HttpResponse:
        self.requests.append(request)
        return self.response


def test_get_current_prices_requests_albion_endpoint() -> None:
    network_client = _FakeNetworkClient(
        HttpResponse(
            status_code=200,
            headers={},
            body=b"[]",
        )
    )
    client = AlbionCurrentPriceClient(
        network_client,
        "https://west.albion-online-data.com/",
    )

    observations: Sequence[CurrentPriceObservation] = client.get_current_prices(
        item_ids=[AlbionItemId("T4_BAG")],
        locations=[AlbionLocation("Caerleon")],
        qualities=[AlbionQuality(1)],
    )

    assert observations == ()
    assert network_client.requests == [
        HttpRequest(
            method="GET",
            url="https://west.albion-online-data.com/api/v2/stats/prices/T4_BAG.json",
            params={"locations": "Caerleon", "qualities": "1"},
        )
    ]


def test_get_current_prices_raises_for_http_error() -> None:
    network_client = _FakeNetworkClient(
        HttpResponse(
            status_code=429,
            headers={},
            body=b"rate limited",
        )
    )
    client = AlbionCurrentPriceClient(
        network_client,
        "https://west.albion-online-data.com",
    )

    with pytest.raises(AlbionApiError, match="429"):
        _ = client.get_current_prices(
            item_ids=[AlbionItemId("T4_BAG")],
            locations=[AlbionLocation("Caerleon")],
        )
