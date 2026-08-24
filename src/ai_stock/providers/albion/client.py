from collections.abc import Collection, Sequence
from datetime import date

from ai_stock.market.types import CurrentPriceObservation, HistoricalPriceObservation
from ai_stock.network.client import NetworkClient
from ai_stock.network.types import HttpMethod, HttpRequest
from ai_stock.providers.albion.parser import (
    parse_current_prices,
    parse_historical_prices,
)
from ai_stock.providers.albion.types import (
    AlbionHistoryInterval,
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class AlbionApiError(RuntimeError):
    """Raised when the Albion API returns an unsuccessful HTTP response."""


class AlbionMarketDataClient:
    def __init__(self, network_client: NetworkClient, base_url: str) -> None:
        self._network_client: NetworkClient = network_client
        self._base_url: str = base_url.rstrip("/")

    def get_current_prices(
        self,
        item_ids: Collection[AlbionItemId],
        locations: Collection[AlbionLocation],
        qualities: Collection[AlbionQuality] = (),
    ) -> Sequence[CurrentPriceObservation]:
        response = self._network_client.request(
            HttpRequest(
                method=HttpMethod.GET,
                url=f"{self._base_url}/api/v2/stats/prices/{','.join(item_ids)}.json",
                params={
                    "locations": ",".join(locations),
                    "qualities": ",".join(str(quality) for quality in qualities),
                },
            )
        )

        if not 200 <= response.status_code < 300:
            raise AlbionApiError(
                f"Albion current price request failed with status {response.status_code}"
            )

        return parse_current_prices(response.body)

    def get_historical_prices(
        self,
        item_ids: Collection[AlbionItemId],
        locations: Collection[AlbionLocation],
        interval: AlbionHistoryInterval | int,
        qualities: Collection[AlbionQuality] = (),
        start: date | None = None,
        end: date | None = None,
    ) -> Sequence[HistoricalPriceObservation]:
        try:
            history_interval = AlbionHistoryInterval(interval)
        except ValueError as error:
            raise ValueError(
                f"Unsupported Albion history interval: {interval}"
            ) from error

        params = {
            "locations": ",".join(locations),
            "qualities": ",".join(str(quality) for quality in qualities),
            "time-scale": str(history_interval.value),
        }
        if start is not None:
            params["date"] = start.isoformat()
        if end is not None:
            params["end_date"] = end.isoformat()

        response = self._network_client.request(
            HttpRequest(
                method=HttpMethod.GET,
                url=f"{self._base_url}/api/v2/stats/history/{','.join(item_ids)}.json",
                params=params,
            )
        )

        if not 200 <= response.status_code < 300:
            raise AlbionApiError(
                f"Albion historical price request failed with status {response.status_code}"
            )

        return parse_historical_prices(response.body)
