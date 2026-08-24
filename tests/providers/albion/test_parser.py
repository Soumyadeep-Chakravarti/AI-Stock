from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from ai_stock.market.types import InstrumentId, MarketId
from ai_stock.providers.albion.parser import AlbionParseError, parse_current_prices


@pytest.fixture
def current_prices_body() -> bytes:
    fixture_path = Path(__file__).parent / "fixtures" / "current_prices.json"
    return fixture_path.read_bytes()


def test_parse_current_prices(current_prices_body: bytes) -> None:
    observations = parse_current_prices(current_prices_body)

    assert observations[0].instrument_id == InstrumentId("T4_BAG")
    assert observations[0].market_id == MarketId("Caerleon")
    assert observations[0].bid_price == Decimal(3521)
    assert observations[0].bid_observed_at == datetime(
        2026,
        8,
        24,
        1,
        5,
        tzinfo=UTC,
    )
    assert observations[0].ask_price == Decimal(5981)
    assert observations[0].ask_observed_at == datetime(
        2026,
        8,
        24,
        6,
        40,
        tzinfo=UTC,
    )


def test_parse_current_prices_treats_zero_price_as_missing_quote(
    current_prices_body: bytes,
) -> None:
    observations = parse_current_prices(current_prices_body)

    assert observations[1].market_id == MarketId("Bridgewatch")
    assert observations[1].ask_price is None
    assert observations[1].ask_observed_at is None


def test_parse_current_prices_rejects_non_list_payload() -> None:
    with pytest.raises(AlbionParseError, match="Expected a list"):
        _ = parse_current_prices(b"{}")


def test_parse_current_prices_rejects_missing_required_field() -> None:
    body = b"""
    [
        {
            "item_id": "T4_BAG"
        }
    ]
    """

    with pytest.raises(AlbionParseError, match="Missing required field"):
        _ = parse_current_prices(body)
