from src.db.exceptions import ClientResponseError
from external_clients import FinanceApiClient
from external_clients.typing import HandleMessage
from telegram_bot.utils import send_telegram_message, get_telegram_user_id
from .abc_handler import AbcHandler


class DeleteCategoryHandler(AbcHandler):
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
        _, _, category_name, _ = message.data.split(":")

        response = (
            f"✅The category '{category_name}' was successfully deleted.\n"
            f"<i>Please click on the 'refresh' button.</i>"
        )

        try:
            await self._finance_api_client.delete_category(
                user_id=user_id,
                category_name=category_name,
            )
        except ClientResponseError:
            response = "❌Server error! (enter a command /help)"

        await send_telegram_message(
            message=message,
            message_text=response,
            is_update_text=is_update,
            is_delete_message=True,
        )
