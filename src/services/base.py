from sys import stderr
from loguru import logger
from src.configs import SettingBot, config_map


def setting_logger() -> None:
    logger.configure(**config_map)
    logger.add(stderr, format="{time} {level} {message}", filter="sub.module", level="INFO")


def loading_arguments(args: SettingBot) -> None:
    def print_logs(is_check_result: bool, argument_name: str) -> None:
        if not is_check_result:
            logger.error(f"Please, check '{argument_name}' env variable.")
            raise KeyError
        logger.debug(f"The '{argument_name}' env variable has been loaded!")

    print_logs(args.is_load(args.TOKEN), "TELEGRAM_BOT_TOKEN")
    print_logs(args.is_load(args.PROXY_URL), "TELEGRAM_PROXY_URL")
    print_logs(args.is_load(args.PROXY_LOGIN), "TELEGRAM_PROXY_LOGIN")
    print_logs(args.is_load(args.PROXY_PASSWORD), "TELEGRAM_PROXY_PASSWORD")
    print_logs(args.is_load(args.TIMEOUT_DELETE_MESSAGE), "TIMEOUT_DELETE_MESSAGE")
