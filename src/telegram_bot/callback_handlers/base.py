from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from configs import ContainerWithStaticText as M
from telegram_bot.utils import (
    send_telegram_message,
    get_telegram_user_id,
    get_telegram_user_name,
    get_telegram_user_link,
)

router = Router(name=__name__)


@router.message(CommandStart(), flags={"middlewares": ["DIMiddleware"]})
async def command_start(
    message: Message,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        user_name = get_telegram_user_name(message)
        user_link = get_telegram_user_link(message)
        await send_telegram_message(
            message=message,
            message_text=M.HELLO % (user_link, user_name),
        )
        logger.debug(f"The user #{user_id} executed the /start command.")
    except Exception as error:
        logger.exception(error)


@router.message(Command("help"), flags={"middlewares": ["DIMiddleware"]})
async def command_help(
    message: Message,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        user_name = get_telegram_user_name(message)
        user_link = get_telegram_user_link(message)
        await send_telegram_message(
            message=message,
            message_text=f"{M.HELLO % (user_link, user_name)}{M.LIST_COMMANDS}",
        )
        logger.debug(f"The user #{user_id} executed the /help command.")
    except Exception as error:
        logger.exception(error)


@router.message(F.text, flags={"middlewares": ["DIMiddleware"]})
async def custom_text(
    message: Message,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        logger.debug(f"The user #{user_id} entered a message.")
    except Exception as error:
        logger.exception(error)
