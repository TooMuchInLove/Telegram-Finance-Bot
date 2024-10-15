from asyncio import run as asyncio_run
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from loguru import logger

from configs import setting_bot, LogBot as LB
from services import setting_logger, loading_arguments
from telegram_bot.routers import router
from telegram_bot.ui import set_default_menu
from bot import TelegramBot


async def main() -> None:
    dp = Dispatcher()
    dp["settings"] = setting_bot
    default = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(
        token=setting_bot.TOKEN,
        default=default,
    )
    telegram_bot = TelegramBot(dp=dp)

    dp.startup.register(telegram_bot.register_handlers)
    dp.include_router(router)

    await set_default_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setting_logger()
        loading_arguments(setting_bot)
        logger.info(LB.SUCCESS_START)
        asyncio_run(main())
    except KeyboardInterrupt:
        logger.warning(LB.WARNING_DISABLE)
    except Exception as err:
        logger.exception(err)
    finally:
        logger.info(LB.SUCCESS_STOP)
