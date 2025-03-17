from loguru import logger
from asyncio import TimeoutError as AsyncioTimeoutError
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from json import dumps as json_dumps
from typing import Any, Self

import aiohttp
from aiohttp import hdrs, web
from yarl import URL

from db.helpers import BaseModel

ResponseType = str | list | dict | dict[str, list]


class _HandleErrorsResult(Enum):
    RETRY = "retry"
    FAIL = "fail"


class ApiClient:
    API_URL: str = ""
    DEFAULT_DELAY = 5

    def __init__(
        self,
        base_url: str = None,
        rate_limit_enabled: bool = True,
        default_delay: int = None,
        max_tries: int = 3,
        proxy: str | None = None,
        timeout: int = 10,
        login: str | None = None,
        password: str | None = None,
        raise_for_status: bool = False,
    ) -> None:
        if base_url:
            self.API_URL = base_url
        self._api_url = URL(self.API_URL)
        if not self.API_URL:
            raise AssertionError("API url must be set in inheritors.")
        if default_delay is None:
            default_delay = self.DEFAULT_DELAY
        self._default_delay = default_delay
        self._rate_limit_enabled = rate_limit_enabled
        self._max_tries = max_tries
        self.__session = None
        self._proxy = proxy
        self._timeout = timeout
        self._auth = None
        if login or password:
            self._auth = aiohttp.BasicAuth(
                login=login or "",
                password=password or "",
            )
        self._raise_for_status = raise_for_status

    @property
    def _session(self) -> aiohttp.ClientSession:
        if not self.__session:
            self.__session = aiohttp.ClientSession(
                raise_for_status=self._raise_for_status,
                timeout=aiohttp.ClientTimeout(self._timeout),
                json_serialize=_dumps,
                headers={"Connection": "Keep-Alive"},
                auth=self._auth,
            )
        return self.__session

    async def close(self) -> None:
        await self._session.close()

    async def _request(  # noqa: C901
        self,
        method: str,
        path: str | None = "",
        params: dict | list[tuple[str, Any]] | None = None,
        data: object | None = None,
        json: object | None = None,
        headers: dict | None = None,
    ) -> ResponseType:
        uri = self._api_url / path if path else self._api_url
        if params:
            params = await _prepare_params(params)
        for i in range(self._max_tries):
            response: aiohttp.ClientResponse | None = None
            try:
                response = await self._session.request(
                    method,
                    uri,
                    params=params,
                    json=json,
                    data=data,
                    headers=headers,
                    proxy=self._proxy,
                )
            except (AsyncioTimeoutError, aiohttp.ClientError) as exc:
                res = self._handle_errors(exc=exc, current_try=i)
                if res == _HandleErrorsResult.FAIL:
                    raise
            else:
                return await self._get_response_body(response)
            finally:
                if response:
                    response.release()
        raise AssertionError("You're not supposed to be here")

    @staticmethod
    async def _get_response_body(response: aiohttp.ClientResponse) -> ResponseType:
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            return await response.text()

    def _handle_errors(
        self,
        exc: AsyncioTimeoutError | aiohttp.ClientError,
        current_try: int,
    ) -> _HandleErrorsResult:
        delay = self._default_delay
        if isinstance(exc, aiohttp.ClientResponseError):
            if exc.status == web.HTTPTooManyRequests.status_code:
                delay = int(exc.headers.get("Retry-After", delay))
                logger.warning(
                    "Too many requests. Retry after {delay}",
                    delay=delay,
                )
            elif exc.status >= 500:
                delay = self._default_delay
                logger.warning(
                    "Service unavailable. Retry after {delay}",
                    delay=delay,
                )
            else:
                return _HandleErrorsResult.FAIL
        else:
            logger.warning(
                f"Error while connecting to service {self.API_URL}. Retry after {delay}. Exc: {str(exc)} {exc}",
            )

        if current_try < (self._max_tries - 1):
            return _HandleErrorsResult.RETRY

        return _HandleErrorsResult.FAIL

    async def _get(
        self,
        path: str,
        headers: dict[str, Any] = None,
        params: list[tuple[str, Any]] = None,
        **kwargs,
    ) -> ResponseType:
        return await self._request(
            method=hdrs.METH_GET,
            path=path,
            params=params if params else kwargs,
            headers=headers,
        )

    async def _post(
        self,
        path: str | None = "",
        headers: dict[str, Any] = None,
        is_json: bool = True,
        **kwargs,
    ) -> ResponseType:
        return await self._request(
            method=hdrs.METH_POST,
            path=path,
            headers=headers,
            json=kwargs if is_json else None,
            data=kwargs if not is_json else None,
        )

    async def _delete(
        self,
        path: str | None = "",
        headers: dict[str, Any] = None,
        is_json: bool = True,
        **kwargs,
    ) -> ResponseType:
        return await self._request(
            method=hdrs.METH_DELETE,
            path=path,
            headers=headers,
            json=kwargs if is_json else None,
            data=kwargs if not is_json else None,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


async def _prepare_params(
    params: dict | list[tuple[str, Any]],
) -> list[tuple[str, Any]]:
    if isinstance(params, dict):
        params = params.items()
    return [
        (k, v if (isinstance(v, str) or type(v) is int) else json_dumps(v))
        for k, v in params
    ]


def _dumps(obj: dict | BaseModel) -> str:
    if isinstance(obj, BaseModel):
        return obj.json()
    return json_dumps(obj, default=default_handler)


def default_handler(
    obj: Decimal | date | datetime | BaseModel,
) -> float | str | dict:
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return str(obj)
    if isinstance(obj, date):
        return str(obj)
    if isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError
