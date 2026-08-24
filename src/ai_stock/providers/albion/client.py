from collections.abc import Collection, Sequence

from ai_stock.market.types import CurrentPriceObservation
from ai_stock.network.client import NetworkClient
from ai_stock.network.types import HttpMethod, HttpRequest
from ai_stock.providers.albion.parser import parse_current_prices
from ai_stock.providers.albion.types import (
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class AlbionApiError(RuntimeError):
    """Raised when the Albion API returns an unsuccessful HTTP response."""


class AlbionCurrentPriceClient:
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
