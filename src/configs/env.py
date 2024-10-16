from os import environ as os_environ
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SettingBot:
    """Settings class for Bot."""

    TOKEN = os_environ.get("TELEGRAM_BOT_TOKEN")
    NAME = os_environ.get("TELEGRAM_BOT_NAME")
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


@dataclass(slots=True, frozen=True)
class SettingsDataBase:
    """Settings class for Data Base."""

    HOST = os_environ.get("DATABASE_HOST")
    PORT = os_environ.get("DATABASE_PORT")
    USER = os_environ.get("DATABASE_USER")
    PASSWORD = os_environ.get("DATABASE_PASSWORD")
    NAME = os_environ.get("DATABASE_NAME")
    POOL_MIN_SIZE = os_environ.get("DATABASE_POOL_MIN_SIZE")
    POOL_MAX_SIZE = os_environ.get("DATABASE_POOL_MAX_SIZE")
    COMMAND_TIMEOUT = os_environ.get("DATABASE_COMMAND_TIMEOUT")

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


setting_bot = SettingBot()

setting_data_base = SettingsDataBase()
