from aiogram import Dispatcher

from src.external_clients import FinanceApiClient
from src.telegram_bot.middlewares import DIMiddleware


class TelegramBot:
    def __init__(
        self,
        dp: Dispatcher,
        finance_api_client: FinanceApiClient,
    ) -> None:
        self._dp = dp
        self._finance_api_client = finance_api_client

    async def register_handlers(self) -> None:
        await self.setup_di()
        self._dp.message.middleware(DIMiddleware(di=self._dp["di"]))
        self._dp.callback_query.middleware(DIMiddleware(di=self._dp["di"]))

    async def setup_di(self) -> None:
        self._dp["di"] = {
            "setting_bot": self._dp["setting_bot"],
        }
        self._dp["finance_api_client"] = self._finance_api_client
