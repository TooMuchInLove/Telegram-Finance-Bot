from os import environ as os_environ
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SettingBot:
    # The name of the bot: @FyodorovBot
    # Bot token from Telegram @BotFather
    TOKEN = os_environ.get("TELEGRAM_BOT_TOKEN")
    # For proxy server
    PROXY_URL = os_environ.get("TELEGRAM_PROXY_URL")
    PROXY_LOGIN = os_environ.get("TELEGRAM_PROXY_LOGIN")
    PROXY_PASSWORD = os_environ.get("TELEGRAM_PROXY_PASSWORD")
    TIMEOUT_DELETE_MESSAGE = int(
        os_environ.get("TELEGRAM_TIMEOUT_DELETE_MESSAGE")
    )

    @staticmethod
    def is_load(argument: str | int) -> bool:
        if argument is None:
            return False
        return True


setting_bot = SettingBot()
