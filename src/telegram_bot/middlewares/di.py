from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject


class DIMiddleware(BaseMiddleware):
    def __init__(self, di: dict) -> None:
        super().__init__()
        self._di = di

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        if not is_middleware_necessary(self, data):
            return await handler(event, data)

        for param in data["handler"].params:
            if param in self._di:
                data[param] = (
                    self._di[param]() if callable(self._di[param]) else self._di[param]
                )

        return await handler(event, data)


def is_middleware_necessary(
    middleware_obj: BaseMiddleware,
    contextual_data: dict,
) -> bool:
    return type(middleware_obj).__name__ in get_flag(
        contextual_data,
        "middlewares",
        default=[],
    )
