from src.db.exceptions import ClientResponseError
from external_clients import FinanceApiClient
from external_clients.typing import HandleMessage
from telegram_bot.ui import get_inline_buttons_for_categories
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
        message: HandleMessage,
        is_update: bool = False,
    ) -> None:
        user_id = get_telegram_user_id(message=message)
        data_for_buttons = []

        try:
            response = await self._finance_api_client.get_categories(user_id=user_id)

            if not response["items"]:
                response = "‼️You don't have any categories."
            else:
                data_for_buttons = [
                    [
                        {"name": category["name"], "account_id": category["accountId"]},
                        {"name": category["name"], "account_id": category["accountId"]},
                        {"name": category["name"], "account_id": category["accountId"]},
                    ]
                    for category in response["items"]
                ]
                response = f"✅<b>Your categories</b>:\n"
        except ClientResponseError:
            response = "❌Server error! (enter a command /help)"

        await send_telegram_message(
            message=message,
            message_text=response,
            is_update_text=is_update,
            buttons=get_inline_buttons_for_categories(data=data_for_buttons),
        )
