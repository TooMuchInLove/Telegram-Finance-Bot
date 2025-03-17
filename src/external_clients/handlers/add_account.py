from configs import setting_bot
from src.db.exceptions import ClientResponseError
from external_clients import FinanceApiClient
from external_clients.typing import HandleMessage
from telegram_bot.ui import get_inline_buttons_for_main_list
from telegram_bot.utils import (
    get_telegram_user_id,
    get_telegram_user_name,
    get_telegram_user_link,
    get_telegram_user_nick,
    send_telegram_message,
)
from .abc_handler import AbcHandler


class AddAccountHandler(AbcHandler):
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
        user_name = get_telegram_user_name(message=message)
        user_link = get_telegram_user_link(message=message)
        nick_name = get_telegram_user_nick(message=message)

        response = (
            f"Hello, <a href='{user_link}'>{user_name}</a>\n"
            f"I'm a bot @{setting_bot.NAME}\n\n"
            "<b>Check out the list of my commands</b>:\n"
            "(Getting started: /start)\n"
            # "1. Enter category: /add_category 'category_name'\n"
            # "2. View the list of current categories: /get_categories\n"
            # "3. View the status of the accounts: /account\n"
            "4. View expenses for the day/month: /day_expenses /monthly_expenses\n"
            "5. View earnings for the day/month: /daily_income /monthly_income\n"
            "6. Enter expenses: /add_expenses\n"
            "7. Enter the income: /add_income\n"
        )

        try:
            await self._finance_api_client.add_account(
                user_id=user_id,
                user_name=nick_name,
            )
        except ClientResponseError:
            response = "❌Server error! (enter a command /help)"

        await send_telegram_message(
            message=message,
            message_text=response,
            is_update_text=is_update,
            buttons=get_inline_buttons_for_main_list(),
        )
