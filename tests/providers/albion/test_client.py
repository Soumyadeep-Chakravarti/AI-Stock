from collections.abc import Sequence
from datetime import date

import pytest

from ai_stock.market.types import CurrentPriceObservation, HistoricalPriceObservation
from ai_stock.network.types import HttpRequest, HttpResponse
from ai_stock.providers.albion.client import AlbionApiError, AlbionMarketDataClient
from ai_stock.providers.albion.types import (
    AlbionHistoryInterval,
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
    client = AlbionMarketDataClient(
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
    client = AlbionMarketDataClient(
        network_client,
        "https://west.albion-online-data.com",
    )

    with pytest.raises(AlbionApiError, match="429"):
        _ = client.get_current_prices(
            item_ids=[AlbionItemId("T4_BAG")],
            locations=[AlbionLocation("Caerleon")],
        )


def test_get_historical_prices_requests_albion_endpoint() -> None:
    network_client = _FakeNetworkClient(
        HttpResponse(
            status_code=200,
            headers={},
            body=b"[]",
        )
    )
    client = AlbionMarketDataClient(
        network_client,
        "https://west.albion-online-data.com",
    )

    observations: Sequence[HistoricalPriceObservation] = client.get_historical_prices(
        item_ids=[AlbionItemId("T4_BAG")],
        locations=[AlbionLocation("Caerleon")],
        qualities=[AlbionQuality(1)],
        interval=AlbionHistoryInterval.DAY,
        start=date(2026, 8, 1),
        end=date(2026, 8, 2),
    )

    assert observations == ()
    assert network_client.requests == [
        HttpRequest(
            method="GET",
            url="https://west.albion-online-data.com/api/v2/stats/history/T4_BAG.json",
            params={
                "locations": "Caerleon",
                "qualities": "1",
                "time-scale": "24",
                "date": "2026-08-01",
                "end_date": "2026-08-02",
            },
        )
    ]


def test_get_historical_prices_rejects_unsupported_interval() -> None:
    network_client = _FakeNetworkClient(
        HttpResponse(
            status_code=200,
            headers={},
            body=b"[]",
        )
    )
    client = AlbionMarketDataClient(
        network_client,
        "https://west.albion-online-data.com",
    )

    with pytest.raises(ValueError, match="Unsupported Albion history interval"):
        _ = client.get_historical_prices(
            item_ids=[AlbionItemId("T4_BAG")],
            locations=[AlbionLocation("Caerleon")],
            interval=15,
        )

    assert network_client.requests == []
