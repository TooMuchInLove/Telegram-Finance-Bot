from aiogram.types import CallbackQuery, Message
from aiohttp import ClientResponseError as AiohttpClientResponseError

from external_clients import FinanceApiClient
from telegram_bot.utils import send_telegram_message, get_telegram_user_id
from .abc_handler import AbcHandler


class GetCategoriesHandler(AbcHandler):
    def __init__(
        self,
        finance_api_client: FinanceApiClient,
    ) -> None:
        self._finance_api_client = finance_api_client

    async def handle(
        self,
        message: Message | CallbackQuery,
        is_update: bool = False,
    ) -> None:
        user_id = get_telegram_user_id(message=message)

        try:
            response = await self._finance_api_client.get_categories(user_id=user_id)

            if not response["items"]:
                response = "‼️You don't have any categories."
            else:
                categories = [f"\n<b>{category['name']}</b>" for category in response["items"]]
                response = f"✅Your categories:\n{' '.join(categories)}"
        except AiohttpClientResponseError:
            response = "❌Server error! (enter a command /help)"

        await send_telegram_message(
            message=message,
            message_text=response,
        )
