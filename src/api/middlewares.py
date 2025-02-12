from asyncio import CancelledError as AsyncioCancelledError
from aiohttp.web import (
    StreamResponse as WebStreamResponse,
    HTTPRequestTimeout as WebHttpRequestTimeout,
    middleware as web_middleware,
)
from aiohttp.abc import Request
from typing import Callable


@web_middleware
async def suppress_cancelled_error_middleware(request: Request, handler: Callable) -> WebStreamResponse:
    """Suppress CancelledError and replace it with HTTPRequestTimeoutError."""

    try:
        return await handler(request)
    except AsyncioCancelledError as exc:
        raise WebHttpRequestTimeout(text=str(exc))
