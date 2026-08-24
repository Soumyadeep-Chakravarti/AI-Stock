from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


def _empty_string_mapping() -> dict[str, str]:
    return {}


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass(frozen=True, slots=True)
class HttpRequest:
    method: HttpMethod
    url: str
    headers: Mapping[str, str] = field(default_factory=_empty_string_mapping)
    params: Mapping[str, str] = field(default_factory=_empty_string_mapping)
    body: bytes | None = None


@dataclass(frozen=True, slots=True)
class HttpResponse:
    status_code: int
    headers: Mapping[str, str]
    body: bytes
