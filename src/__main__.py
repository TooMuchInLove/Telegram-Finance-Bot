from asyncio import run as asyncio_run
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger

from configs import (
    config_map,
    SettingBase,
    SettingBot,
    SettingsDataBase,
    setting_base,
    setting_bot,
    setting_data_base,
    check_envs_the_loading,
)
from external_clients import FinanceApiClient
from telegram_bot.routers import router
from telegram_bot.ui import set_default_menu
from bot import TelegramBot


def setting_logger() -> None:
    logger.configure(**config_map)


async def main() -> None:
    dp = Dispatcher()
    dp["setting_bot"] = setting_bot
    dp["setting_db"] = setting_data_base
    default = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(
        token=setting_bot.TOKEN,
        default=default,
    )
    finance_api_client = FinanceApiClient(
        api_url=setting_base.FINANCE_API_CLIENT_URL,
    )
    telegram_bot = TelegramBot(
        dp=dp,
        finance_api_client=finance_api_client,
    )

    dp.startup.register(telegram_bot.register_handlers)
    dp.include_router(router)

    await set_default_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    setting_logger()
    check_envs_the_loading(instances=[SettingBase, SettingBot, SettingsDataBase])
    logger.info("Starting...")
    try:
        asyncio_run(main())
    except KeyboardInterrupt:
        logger.warning("The bot is disabled.")
    except Exception as err:
        logger.exception(err)
    finally:
        logger.info("Stopping...")
