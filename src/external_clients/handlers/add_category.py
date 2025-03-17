from src.db.exceptions import ClientResponseError
from external_clients import FinanceApiClient
from external_clients.typing import HandleMessage
from telegram_bot.utils import send_telegram_message, get_telegram_user_id, get_the_entered_words
from .abc_handler import AbcHandler


class AddCategoryHandler(AbcHandler):
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
        words = get_the_entered_words(message=message)
        if len(words) == 1:
            return await send_telegram_message(
                message=message,
                message_text="‼️Enter the name of the category!",
                is_update_text=is_update,
            )

        category_name = " ".join(words[1:])
        user_id = get_telegram_user_id(message=message)

        response = "✅The category name has been added."

        try:
            await self._finance_api_client.add_category(
                user_id=user_id,
                category_name=category_name,
            )
        except ClientResponseError:
            response = "❌Server error! (enter a command /help)"

        await send_telegram_message(
            message=message,
            message_text=response,
            is_update_text=is_update,
        )
