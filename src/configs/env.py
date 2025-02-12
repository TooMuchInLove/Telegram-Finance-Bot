from os import environ as os_environ
from dataclasses import dataclass
from loguru import logger


@dataclass(slots=True, frozen=True)
class Settings:
    """Main Settings class."""

    @staticmethod
    def print_logs(argument: str | int, argument_name: str) -> None:
        if argument is None:
            logger.error(f"Please, check '{argument_name}' env variable.")
            raise KeyError
        logger.debug(f"The '{argument_name}' env variable has been loaded!")


@dataclass(slots=True, frozen=True)
class SettingBase(Settings):
    """Base Settings class."""

    WEB_PORT = int(os_environ.get("BASE_WEB_PORT"))
    WEB_APP_URL = os_environ.get("BASE_WEB_APP_URL")
    FINANCE_API_CLIENT_URL = os_environ.get("BASE_FINANCE_API_CLIENT_URL")

    def checking_the_loading_of_arguments(self) -> None:
        self.print_logs(self.WEB_PORT, "BASE_WEB_PORT")
        self.print_logs(self.FINANCE_API_CLIENT_URL, "BASE_FINANCE_API_CLIENT_URL")


@dataclass(slots=True, frozen=True)
class SettingBot(Settings):
    """Settings class for Bot."""

    TOKEN = os_environ.get("TELEGRAM_BOT_TOKEN")
    NAME = os_environ.get("TELEGRAM_BOT_NAME")
    PROXY_URL = os_environ.get("TELEGRAM_PROXY_URL")
    PROXY_LOGIN = os_environ.get("TELEGRAM_PROXY_LOGIN")
    PROXY_PASSWORD = os_environ.get("TELEGRAM_PROXY_PASSWORD")
    TIMEOUT_DELETE_MESSAGE = int(os_environ.get("TELEGRAM_TIMEOUT_DELETE_MESSAGE"))

    def checking_the_loading_of_arguments(self) -> None:
        self.print_logs(self.TOKEN, "TELEGRAM_BOT_TOKEN")
        self.print_logs(self.PROXY_URL, "TELEGRAM_PROXY_URL")
        self.print_logs(self.PROXY_LOGIN, "TELEGRAM_PROXY_LOGIN")
        self.print_logs(self.PROXY_PASSWORD, "TELEGRAM_PROXY_PASSWORD")
        self.print_logs(self.TIMEOUT_DELETE_MESSAGE, "TELEGRAM_TIMEOUT_DELETE_MESSAGE")


@dataclass(slots=True, frozen=True)
class SettingsDataBase(Settings):
    """Settings class for Data Base."""

    HOST = os_environ.get("DATABASE_HOST")
    PORT = int(os_environ.get("DATABASE_PORT"))
    USER = os_environ.get("DATABASE_USER")
    PASSWORD = os_environ.get("DATABASE_PASSWORD")
    NAME = os_environ.get("DATABASE_NAME")
    POOL_MIN_SIZE = int(os_environ.get("DATABASE_POOL_MIN_SIZE"))
    POOL_MAX_SIZE = int(os_environ.get("DATABASE_POOL_MAX_SIZE"))
    COMMAND_TIMEOUT = int(os_environ.get("DATABASE_COMMAND_TIMEOUT"))

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    def checking_the_loading_of_arguments(self) -> None:
        self.print_logs(self.HOST, "DATABASE_HOST")
        self.print_logs(self.PORT, "DATABASE_PORT")
        self.print_logs(self.USER, "DATABASE_USER")
        self.print_logs(self.PASSWORD, "DATABASE_PASSWORD")
        self.print_logs(self.NAME, "DATABASE_NAME")
        self.print_logs(self.POOL_MIN_SIZE, "DATABASE_POOL_MIN_SIZE")
        self.print_logs(self.POOL_MAX_SIZE, "DATABASE_POOL_MAX_SIZE")
        self.print_logs(self.COMMAND_TIMEOUT, "DATABASE_COMMAND_TIMEOUT")


setting_base = SettingBase()

setting_bot = SettingBot()

setting_data_base = SettingsDataBase()
