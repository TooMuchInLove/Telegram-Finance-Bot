from loguru import logger
from aiohttp.abc import AbstractAccessLogger


class RequestLogger(AbstractAccessLogger):
    """Logger for aiohttp requests."""

    def log(self, request, response, time) -> None:
        """Emit log to logger."""

        if request.path.startswith("/healthcheck"):
            return

        if request.headers.get("allowLogging") == "false":
            return
        logger.info(f"{request.method} {request.path} {response.status} in {time} sec")
