from os import environ as os_environ
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SettingBot:
    # The name of the bot: @FyodorovBot
    # Bot token from Telegram @BotFather
    TOKEN = os_environ.get("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = os_environ.get("TELEGRAM_CHANNEL_ID")

    @staticmethod
    def is_load(argument) -> bool:
        if argument is None:
            return False
        return True


setting_bot = SettingBot()
