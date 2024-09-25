from __future__ import annotations

import typing

from selectolax.parser import HTMLParser, Node, Selector
from httpx._models import Response

from ._broadcaster import BroadcastList

if typing.TYPE_CHECKING:
    from ._broadcaster import NodeBroadcastList

__all__ = ["CSSTool", "CSSResponse"]

T = typing.TypeVar("T")
_ABSENT = object()


class CSSTool:
    __slots__ = "text", "_cache"

    def __init__(self, text: str | None) -> None:
        if text is not None:
            self.text: str = text

    def parse(self, *, new: bool = False, refresh: bool = False) -> HTMLParser:
        if refresh:
            self._cache = HTMLParser(self.text)

        if new:
            return HTMLParser(self.text)

        try:
            return self._cache
        except AttributeError:
            self._cache = HTMLParser(self.text)
            return self._cache

    def match(self, query: str, *, new: bool = False) -> NodeBroadcastList:
        return BroadcastList(self.parse(new=new).css(query))  # type: ignore

    @typing.overload
    def single(self, query: str, *, remain_ok: bool = False, new: bool = False) -> Node: ...

    @typing.overload
    def single(self, query: str, default: T, *, remain_ok: bool = False, new: bool = False) -> Node | T: ...

    def single(self, query, default=_ABSENT, *, remain_ok=False, new: bool = False):
        css_result = self.parse(new=new).css(query)
        length = len(css_result)

        if length == 0:
            if default is _ABSENT:
                raise ValueError(f"Query {query!r} matched with no nodes {self._get_url_note()}.")
            else:
                return default
        elif remain_ok or length == 1:
            return css_result.pop()
        else:
            raise ValueError(f"Query {query!r} matched with {length} nodes {self._get_url_note()}.")

    def _get_url_note(self) -> str:
        try:
            url = self.url  # type: ignore
        except AttributeError:
            url_note = ""
        else:
            url_note = f"(error from '{url}')"
        return url_note


class CSSResponse(Response, CSSTool):
    def __init__(self, response: Response) -> None:
        self.__dict__ = response.__dict__
