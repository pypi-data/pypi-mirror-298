from __future__ import annotations

import typing
from contextlib import asynccontextmanager, contextmanager

from httpx import AsyncClient as HttpxAsyncClient
from httpx import Client as HttpxClient
from httpx._client import USE_CLIENT_DEFAULT, EventHook, UseClientDefault
from httpx._config import (
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_CONFIG,
    Limits,
)

from ._css import CSSResponse
from ._base import logger

if typing.TYPE_CHECKING:
    # from httpx._models import Request
    from httpx._transports.base import AsyncBaseTransport, BaseTransport
    from httpx._types import (
        AuthTypes,
        CertTypes,
        CookieTypes,
        HeaderTypes,
        ProxiesTypes,
        ProxyTypes,
        QueryParamTypes,
        RequestContent,
        RequestData,
        RequestExtensions,
        RequestFiles,
        TimeoutTypes,
        VerifyTypes,
    )
    from httpx._urls import URL

__all__ = ["AsyncClient", "Client"]


class Client(HttpxClient):
    __slots__ = "retry", "raise_for_status"

    def __init__(
        self,
        *,
        auth: AuthTypes | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        mounts: None | (typing.Mapping[str, BaseTransport | None]) = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: None | (typing.Mapping[str, list[EventHook]]) = None,
        base_url: URL | str = "",
        transport: BaseTransport | None = None,
        app: typing.Callable[..., typing.Any] | None = None,
        trust_env: bool = True,
        default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
        retry: int | None = None,
        raise_for_status: bool = False,
    ) -> None:
        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env,
            default_encoding=default_encoding,
        )
        self.retry = retry
        self.raise_for_status = raise_for_status

    def request(
        self,
        method: str,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        last_exc = None
        retry = retry or self.retry or 1
        for _ in range(retry):
            try:
                response = super().request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )

                # Retry when status code is server error.
                # Exceptions of HTTP 4XX does not trigger retry.
                if raise_for_status and response.status_code >= 500:
                    response.raise_for_status()

            except Exception as exc:
                if retry == 1:
                    raise
                logger.warning("Attempting fetch again...")
                last_exc = exc
            else:
                if last_exc:
                    logger.warning(f"Successfully retrieve {url!r}")

                # If raise_for_status is False, raise_for_status won't be checked.
                if raise_for_status or raise_for_status is None and self.raise_for_status:
                    response.raise_for_status()

                return CSSResponse(response)

        if last_exc is None:
            raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

        raise last_exc

    @contextmanager
    def stream(
        self,
        method: str,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> typing.Iterator[CSSResponse]:
        last_exc = None
        retry = retry or self.retry or 1
        for _ in range(retry):
            try:
                streamer = super().stream(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
            except Exception as exc:
                if retry == 1:
                    raise
                logger.warning("Attempting fetch again...")
                last_exc = exc
            else:
                if last_exc:
                    logger.warning(f"Successfully retrieve {url!r}")

                with streamer as stream:
                    # If raise_for_status is False, raise_for_status won't be checked.
                    if raise_for_status or raise_for_status is None and self.raise_for_status:
                        try:
                            stream.raise_for_status()
                        except Exception as exc:
                            # Exceptions of HTTP 4XX does not trigger retry.
                            if stream.status_code >= 500:
                                last_exc = exc
                                continue
                            raise

                    yield CSSResponse(stream)
                    return

        if last_exc is None:
            raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

        raise last_exc

    # request and stream use send method internally.
    # def send(
    #     self,
    #     request: Request,
    #     *,
    #     stream: bool = False,
    #     auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
    #     follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    #     retry: int | None = None,
    #     raise_for_status: bool | None = None,
    # ) -> CSSResponse:
    #     last_exc = None
    #     for _ in range(retry or self.retry or 1):
    #         try:
    #             response = super().send(
    #                 request,
    #                 stream=stream,
    #                 auth=auth,
    #                 follow_redirects=follow_redirects,
    #             )
    #         except Exception as exc:
    #             if retry == 1:
    #                 raise
    #             logger.warning("Attempting fetch again...")
    #             last_exc = exc
    #         else:
    #             if last_exc:
    #                 logger.warning(f"Successfully retrieve {request!r}")

    #             # Exceptions from raise_for_status does not trigger retry.
    #             if raise_for_status or self.raise_for_status:
    #                 response.raise_for_status()

    #             return CSSResponse(response)

    #     if last_exc is None:
    #         raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

    #     raise last_exc

    def get(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `GET` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def options(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send an `OPTIONS` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def head(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `HEAD` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "HEAD",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def post(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `POST` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def put(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `PUT` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def patch(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `PATCH` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    def delete(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `DELETE` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )


class AsyncClient(HttpxAsyncClient):
    __slots__ = "retry"

    def __init__(
        self,
        *,
        auth: AuthTypes | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        mounts: None | (typing.Mapping[str, AsyncBaseTransport | None]) = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: None | (typing.Mapping[str, list[EventHook]]) = None,
        base_url: URL | str = "",
        transport: AsyncBaseTransport | None = None,
        app: typing.Callable[..., typing.Any] | None = None,
        trust_env: bool = True,
        default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> None:
        super().__init__(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env,
            default_encoding=default_encoding,
        )
        self.retry = retry
        self.raise_for_status = raise_for_status

    async def request(
        self,
        method: str,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        last_exc = None
        retry = retry or self.retry or 1
        for _ in range(retry):
            try:
                response = await super().request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
            except Exception as exc:
                if retry == 1:
                    raise
                logger.warning("Attempting fetch again...")
                last_exc = exc
            else:
                if last_exc:
                    logger.warning(f"Successfully retrieve {url!r}")

                # Exceptions from raise_for_status does not trigger retry.
                if raise_for_status or self.raise_for_status:
                    response.raise_for_status()

                return CSSResponse(response)

        if last_exc is None:
            raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

        raise last_exc

    @asynccontextmanager
    async def stream(
        self,
        method: str,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> typing.AsyncIterator[CSSResponse]:
        last_exc = None
        retry = retry or self.retry or 1
        for _ in range(retry):
            try:
                streamer = super().stream(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
            except Exception as exc:
                if retry == 1:
                    raise
                logger.warning("Attempting fetch again...")
                last_exc = exc
            else:
                if last_exc:
                    logger.warning(f"Successfully retrieve {url!r}")

                async with streamer as stream:
                    # Exceptions from raise_for_status does not trigger retry.
                    # If raise_for_status is False, raise_for_status won't be checked.
                    if raise_for_status or raise_for_status is None and self.raise_for_status:
                        stream.raise_for_status()

                    yield CSSResponse(stream)

        if last_exc is None:
            raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

        raise last_exc

    # request and stream use send method internally.
    # async def send(
    #     self,
    #     request: Request,
    #     *,
    #     stream: bool = False,
    #     auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
    #     follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    #     retry: int | None = None,
    #     raise_for_status: bool | None = None,
    # ) -> CSSResponse:
    #     last_exc = None
    #     retry = retry or self.retry or 1
    #     for _ in range(retry):
    #         try:
    #             response = await super().send(
    #                 request,
    #                 stream=stream,
    #                 auth=auth,
    #                 follow_redirects=follow_redirects,
    #             )
    #         except Exception as exc:
    #             logger.warning("Attempting fetch again...")
    #             last_exc = exc
    #         else:
    #             if last_exc:
    #                 logger.warning(f"Successfully retrieve {request!r}")

    #             # Exceptions from raise_for_status does not trigger retry.
    #             if raise_for_status or self.raise_for_status:
    #                 response.raise_for_status()

    #             return CSSResponse(response)

    #     if last_exc is None:
    #         raise ValueError(f"Retry value must be natural number, but it's {retry!r}")

    #     raise last_exc

    async def get(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `GET` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def options(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send an `OPTIONS` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def head(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `HEAD` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "HEAD",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def post(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `POST` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def put(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `PUT` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def patch(
        self,
        url: URL | str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `PATCH` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )

    async def delete(
        self,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        retry: int | None = None,
        raise_for_status: bool | None = None,
    ) -> CSSResponse:
        """
        Send a `DELETE` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            retry=retry,
            raise_for_status=raise_for_status,
        )
