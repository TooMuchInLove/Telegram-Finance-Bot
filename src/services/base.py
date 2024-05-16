from loguru import logger
from src.configs import SettingBot, config_map


def setting_logger() -> None:
    logger.configure(**config_map)


def loading_arguments(arguments: SettingBot) -> None:
    def print_logs(is_check_result: bool, argument_name: str) -> None:
        if not is_check_result:
            logger.error(f"Please, check '{argument_name}' env variable.")
            raise KeyError
        logger.debug(f"The '{argument_name}' env variable has been loaded!")

    print_logs(arguments.is_load(arguments.TOKEN), "TELEGRAM_BOT_TOKEN")
    print_logs(arguments.is_load(arguments.PROXY_URL), "TELEGRAM_PROXY_URL")
    print_logs(arguments.is_load(arguments.PROXY_LOGIN), "TELEGRAM_PROXY_LOGIN")
    print_logs(arguments.is_load(arguments.PROXY_PASSWORD), "TELEGRAM_PROXY_PASSWORD")
