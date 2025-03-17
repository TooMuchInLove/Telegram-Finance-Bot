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


@dataclass(slots=True, frozen=True)
class SettingBot(Settings):
    """Settings class for Bot."""

    TOKEN = os_environ.get("TELEGRAM_BOT_TOKEN")
    NAME = os_environ.get("TELEGRAM_BOT_NAME")
    PROXY_URL = os_environ.get("TELEGRAM_PROXY_URL")
    PROXY_LOGIN = os_environ.get("TELEGRAM_PROXY_LOGIN")
    PROXY_PASSWORD = os_environ.get("TELEGRAM_PROXY_PASSWORD")
    TIMEOUT_DELETE_MESSAGE = int(os_environ.get("TELEGRAM_TIMEOUT_DELETE_MESSAGE"))


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


def check_envs_the_loading(instances: list[type[Settings]]) -> None:
    for instance in instances:
        fields = [
            v for v in instance.__dict__.keys()
            if not v.startswith("__") and not callable(getattr(instance, v))
        ]
        for field in fields:
            instance.print_logs(argument=getattr(instance, field), argument_name=field)


setting_base = SettingBase()

setting_bot = SettingBot()

setting_data_base = SettingsDataBase()
