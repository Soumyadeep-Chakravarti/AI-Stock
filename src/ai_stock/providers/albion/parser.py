import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

from ai_stock.market.types import (
    CurrentPriceObservation,
    HistoricalPriceObservation,
    InstrumentId,
    MarketId,
)
from ai_stock.providers.albion.types import (
    AlbionCurrentPriceRecord,
    AlbionHistoricalPricePoint,
    AlbionHistoricalPriceRecord,
    AlbionItemId,
    AlbionLocation,
    AlbionQuality,
)


class AlbionParseError(ValueError):
    """Raised when an Albion API response does not match the expected schema."""


def parse_current_prices(body: bytes) -> Sequence[CurrentPriceObservation]:
    try:
        values = _parse_list_payload(body, "current price")
        records = [_parse_current_price_record(value) for value in values]
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        if isinstance(error, AlbionParseError):
            raise
        raise AlbionParseError("Invalid Albion current price response") from error

    return tuple(_to_current_price_observation(record) for record in records)


def parse_historical_prices(body: bytes) -> Sequence[HistoricalPriceObservation]:
    try:
        values = _parse_list_payload(body, "historical price")
        records = [_parse_historical_price_record(value) for value in values]
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        if isinstance(error, AlbionParseError):
            raise
        raise AlbionParseError("Invalid Albion historical price response") from error

    return tuple(
        observation
        for record in records
        for observation in _to_historical_price_observations(record)
    )


def _parse_list_payload(body: bytes, record_type: str) -> list[object]:
    payload = cast(object, json.loads(body))
    if not isinstance(payload, list):
        raise AlbionParseError(f"Expected a list of {record_type} records")
    return cast(list[object], payload)


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


def _parse_historical_price_record(value: object) -> AlbionHistoricalPriceRecord:
    if not isinstance(value, dict):
        raise AlbionParseError("Expected each historical price record to be an object")

    record = cast(Mapping[str, object], value)
    data = _read_list(record, "data")
    return AlbionHistoricalPriceRecord(
        item_id=AlbionItemId(_read_string(record, "item_id")),
        location=AlbionLocation(_read_string(record, "location")),
        quality=AlbionQuality(_read_integer(record, "quality")),
        data=tuple(_parse_historical_price_point(point) for point in data),
    )


def _parse_historical_price_point(value: object) -> AlbionHistoricalPricePoint:
    if not isinstance(value, dict):
        raise AlbionParseError("Expected each historical price point to be an object")

    point = cast(Mapping[str, object], value)
    return AlbionHistoricalPricePoint(
        item_count=_read_integer(point, "item_count"),
        avg_price=_read_integer(point, "avg_price"),
        timestamp=_read_string(point, "timestamp"),
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


def _read_list(record: Mapping[str, object], field: str) -> list[object]:
    try:
        value = record[field]
    except KeyError as error:
        raise AlbionParseError(f"Missing required field: {field}") from error

    if not isinstance(value, list):
        raise AlbionParseError(f"Expected {field} to be a list")
    return cast(list[object], value)


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


def _to_historical_price_observations(
    record: AlbionHistoricalPriceRecord,
) -> Sequence[HistoricalPriceObservation]:
    return tuple(
        HistoricalPriceObservation(
            instrument_id=InstrumentId(record.item_id),
            market_id=MarketId(record.location),
            price=Decimal(point.avg_price),
            observed_at=_parse_timestamp(point.timestamp),
            # Albion reports a sell-order bucket's aggregate item amount.
            quantity=Decimal(point.item_count),
        )
        for point in record.data
    )


def _parse_quote(price: int, timestamp: str) -> tuple[Decimal | None, datetime | None]:
    if price <= 0:
        return None, None
    return Decimal(price), _parse_timestamp(timestamp)


def _parse_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp).replace(tzinfo=UTC)
