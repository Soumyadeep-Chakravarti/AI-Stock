import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

from ai_stock.market.types import CurrentPriceObservation, InstrumentId, MarketId
from ai_stock.providers.albion.types import (
    AlbionCurrentPriceRecord,
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class AlbionParseError(ValueError):
    """Raised when an Albion API response does not match the expected schema."""


def parse_current_prices(body: bytes) -> Sequence[CurrentPriceObservation]:
    try:
        payload = cast(object, json.loads(body))
        if not isinstance(payload, list):
            raise AlbionParseError("Expected a list of current price records")

        values = cast(list[object], payload)
        records = [_parse_current_price_record(value) for value in values]
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        if isinstance(error, AlbionParseError):
            raise
        raise AlbionParseError("Invalid Albion current price response") from error

    return tuple(_to_current_price_observation(record) for record in records)


def _parse_current_price_record(value: object) -> AlbionCurrentPriceRecord:
    if not isinstance(value, dict):
        raise AlbionParseError("Expected each current price record to be an object")

    record = cast(Mapping[str, object], value)
    return AlbionCurrentPriceRecord(
        item_id=AlbionItemId(_read_string(record, "item_id")),
        location=AlbionLocation(_read_string(record, "city")),
        quality=AlbionQuality(_read_integer(record, "quality")),
        sell_price_min=_read_integer(record, "sell_price_min"),
        sell_price_min_date=_read_string(record, "sell_price_min_date"),
        buy_price_max=_read_integer(record, "buy_price_max"),
        buy_price_max_date=_read_string(record, "buy_price_max_date"),
    )


def _read_string(record: Mapping[str, object], field: str) -> str:
    try:
        value = record[field]
    except KeyError as error:
        raise AlbionParseError(f"Missing required field: {field}") from error

    if not isinstance(value, str):
        raise AlbionParseError(f"Expected {field} to be a string")
    return value


def _read_integer(record: Mapping[str, object], field: str) -> int:
    try:
        value = record[field]
    except KeyError as error:
        raise AlbionParseError(f"Missing required field: {field}") from error

    if not isinstance(value, int) or isinstance(value, bool):
        raise AlbionParseError(f"Expected {field} to be an integer")
    return value


def _to_current_price_observation(
    record: AlbionCurrentPriceRecord,
) -> CurrentPriceObservation:
    bid_price, bid_observed_at = _parse_quote(
        record.buy_price_max,
        record.buy_price_max_date,
    )
    ask_price, ask_observed_at = _parse_quote(
        record.sell_price_min,
        record.sell_price_min_date,
    )

    return CurrentPriceObservation(
        instrument_id=InstrumentId(record.item_id),
        market_id=MarketId(record.location),
        bid_price=bid_price,
        bid_observed_at=bid_observed_at,
        ask_price=ask_price,
        ask_observed_at=ask_observed_at,
    )


def _parse_quote(price: int, timestamp: str) -> tuple[Decimal | None, datetime | None]:
    if price <= 0:
        return None, None
    return Decimal(price), datetime.fromisoformat(timestamp).replace(tzinfo=UTC)
