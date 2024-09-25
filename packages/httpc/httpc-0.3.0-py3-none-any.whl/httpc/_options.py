from __future__ import annotations

import sys
import typing
from dataclasses import asdict, dataclass, fields

if typing.TYPE_CHECKING:
    from httpx._client import EventHook
    from httpx._config import Limits
    from httpx._transports.base import BaseTransport
    from httpx._types import (
        AuthTypes,
        CertTypes,
        CookieTypes,
        HeaderTypes,
        ProxiesTypes,
        ProxyTypes,
        QueryParamTypes,
        TimeoutTypes,
        URLTypes,
        VerifyTypes,
    )

from httpc._api import request
from httpc._client import AsyncClient, Client
from httpc._css import CSSResponse

__all__ = [
    "HEADERS",
    "ClientOptions",
    "common",
]

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ko-KR,ko;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}
_REQUEST_KEYS = {
    "params",
    "headers",
    "cookies",
    "auth",
    "proxy",
    "proxies",
    "follow_redirects",
    "cert",
    "verify",
    "timeout",
    "trust_env",
    "attempts",
    "raise_for_status",
}


if sys.version_info >= (3, 10):
    _dataclass_args = {"slots": True}
else:
    _dataclass_args = {}


@dataclass(**_dataclass_args)
class ClientOptions:
    auth: AuthTypes | None = None
    params: QueryParamTypes | None = None
    headers: HeaderTypes | None = None
    cookies: CookieTypes | None = None
    verify: VerifyTypes | None = None
    cert: CertTypes | None = None
    http1: bool | None = None
    http2: bool | None = None
    proxy: ProxyTypes | None = None
    proxies: ProxiesTypes | None = None
    mounts: typing.Mapping[str, BaseTransport | None] | None = None
    timeout: TimeoutTypes = None
    follow_redirects: bool | None = None
    limits: Limits | None = None
    max_redirects: int | None = None
    event_hooks: typing.Mapping[str, list[EventHook]] | None = None
    base_url: URLTypes | None = None
    transport: BaseTransport | None = None
    app: typing.Callable[..., typing.Any] | None = None
    trust_env: bool | None = None
    default_encoding: str | typing.Callable[[bytes], str | None] | None = None
    retry: int | None = None
    raise_for_status: bool | None = None

    def copy(self) -> ClientOptions:
        return ClientOptions(**asdict(self))

    def filled_options(self) -> dict[str, typing.Any]:
        return {name: value for field in fields(self) if (value := getattr(self, name := field.name)) is not None}

    def client(self) -> Client:
        return Client(**self.filled_options())

    def async_client(self) -> AsyncClient:
        return AsyncClient(**self.filled_options())

    def request(self, *args, **kwargs) -> CSSResponse:
        options = {
            key: value
            for key, value in self.filled_options().items()
            if key in _REQUEST_KEYS
        }
        options.update(kwargs)
        return request(*args, **options)

    def get(self, *args, **kwargs) -> CSSResponse:
        return self.request("GET", *args, **kwargs)

    def options(self, *args, **kwargs) -> CSSResponse:
        return self.request("OPTIONS", *args, **kwargs)

    def head(self, *args, **kwargs) -> CSSResponse:
        return self.request("HEAD", *args, **kwargs)

    def post(self, *args, **kwargs) -> CSSResponse:
        return self.request("POST", *args, **kwargs)

    def put(self, *args, **kwargs) -> CSSResponse:
        return self.request("PUT", *args, **kwargs)

    def patch(self, *args, **kwargs) -> CSSResponse:
        return self.request("PATCH", *args, **kwargs)

    def delete(self, *args, **kwargs) -> CSSResponse:
        return self.request("DELETE", *args, **kwargs)


common = ClientOptions(
    headers=HEADERS,
    follow_redirects=True,
    raise_for_status=True,
)
