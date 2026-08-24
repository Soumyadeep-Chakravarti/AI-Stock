from collections.abc import Collection, Sequence
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId
from ai_stock.providers.albion.types import (
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)
from ai_stock.scanner.arbitrage import scan_arbitrage


class _FakeCurrentPriceClient:
    def __init__(self, observations: Sequence[CurrentPriceObservation]) -> None:
        self.observations = observations
        self.calls: list[
            tuple[
                Collection[AlbionItemId],
                Collection[AlbionLocation],
                Collection[AlbionQuality],
            ]
        ] = []

    def get_current_prices(
        self,
        item_ids: Collection[AlbionItemId],
        locations: Collection[AlbionLocation],
        qualities: Collection[AlbionQuality] = (),
    ) -> Sequence[CurrentPriceObservation]:
        self.calls.append((item_ids, locations, qualities))
        return self.observations


def _observation(
    market_id: str,
    *,
    instrument_id: str = "T4_BAG",
    bid_price: int | None,
    bid_observed_at: datetime | None,
    ask_price: int | None,
    ask_observed_at: datetime | None,
) -> CurrentPriceObservation:
    return CurrentPriceObservation(
        instrument_id=InstrumentId(instrument_id),
        market_id=MarketId(market_id),
        bid_price=Decimal(bid_price) if bid_price is not None else None,
        bid_observed_at=bid_observed_at,
        ask_price=Decimal(ask_price) if ask_price is not None else None,
        ask_observed_at=ask_observed_at,
    )


def test_scan_arbitrage_fetches_and_filters_opportunities() -> None:
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    item_ids = [AlbionItemId("T4_BAG"), AlbionItemId("T5_BAG")]
    locations = [
        AlbionLocation("Bridgewatch"),
        AlbionLocation("Caerleon"),
        AlbionLocation("Stale"),
    ]
    qualities = [AlbionQuality(1)]
    client = _FakeCurrentPriceClient(
        [
            _observation(
                "Bridgewatch",
                bid_price=90,
                bid_observed_at=now - timedelta(minutes=10),
                ask_price=100,
                ask_observed_at=now - timedelta(minutes=10),
            ),
            _observation(
                "Caerleon",
                bid_price=125,
                bid_observed_at=now - timedelta(minutes=20),
                ask_price=130,
                ask_observed_at=now - timedelta(minutes=20),
            ),
            _observation(
                "Stale",
                bid_price=150,
                bid_observed_at=now - timedelta(hours=3),
                ask_price=None,
                ask_observed_at=None,
            ),
        ]
    )

    result = scan_arbitrage(
        client,
        item_ids=item_ids,
        locations=locations,
        qualities=qualities,
        now=now,
        max_quote_age=timedelta(hours=2),
        max_timestamp_skew=timedelta(minutes=30),
    )

    assert client.calls == [(item_ids, locations, qualities)]
    assert len(result.opportunities) == 1
    assert result.opportunities[0].buy_market_id == MarketId("Bridgewatch")
    assert result.opportunities[0].sell_market_id == MarketId("Caerleon")

    statuses = {status.market_id: status for status in result.quote_statuses}
    assert statuses[MarketId("Bridgewatch")].bid_present
    assert statuses[MarketId("Bridgewatch")].ask_present
    assert statuses[MarketId("Bridgewatch")].bid_fresh
    assert statuses[MarketId("Bridgewatch")].ask_fresh
    assert statuses[MarketId("Stale")].bid_present
    assert not statuses[MarketId("Stale")].ask_present
    assert not statuses[MarketId("Stale")].bid_fresh
    assert not statuses[MarketId("Stale")].ask_fresh

    coverage = {coverage.instrument_id: coverage for coverage in result.coverage}
    assert coverage[InstrumentId("T4_BAG")].requested_market_count == 3
    assert coverage[InstrumentId("T4_BAG")].returned_record_count == 3
    assert coverage[InstrumentId("T4_BAG")].fresh_bid_count == 2
    assert coverage[InstrumentId("T4_BAG")].fresh_ask_count == 2
    assert coverage[InstrumentId("T4_BAG")].usable_market_count == 2
    assert coverage[InstrumentId("T4_BAG")].usable_market_ratio == Decimal(2) / 3
    assert coverage[InstrumentId("T5_BAG")].returned_record_count == 0
    assert coverage[InstrumentId("T5_BAG")].usable_market_ratio == Decimal(0)
