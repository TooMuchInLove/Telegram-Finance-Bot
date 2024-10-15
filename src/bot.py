from aiogram import Dispatcher

from telegram_bot.middlewares import DIMiddleware


class TelegramBot:
    def __init__(
        self,
        dp: Dispatcher,
    ) -> None:
        self._dp = dp

    async def register_handlers(self) -> None:
        await self.setup_di()
        self._dp.message.middleware(DIMiddleware(di=self._dp["di"]))
        self._dp.callback_query.middleware(DIMiddleware(di=self._dp["di"]))

    async def setup_di(self) -> None:
        self._dp["di"] = {
            "settings": self._dp["settings"],
        }
