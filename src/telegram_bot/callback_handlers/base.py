from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from applications.handlers import (
    AddAccountHandler,
)
from external_clients import (
    FinanceApiClient,
    AddAccountHandler,
    AddCategoryHandler,
    GetCategoriesHandler,
)
from telegram_bot.utils import get_telegram_user_id

router = Router(name=__name__)


@router.message(CommandStart(), flags={"middlewares": ["DIMiddleware"]})
async def command_start(
    message: Message,
    finance_api_client: FinanceApiClient,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await AddAccountHandler(finance_api_client).handle(message)
        logger.debug(f"The user #{user_id} executed the /start command.")
    except Exception as error:
        logger.exception(error)


@router.message(Command("add_category"), flags={"middlewares": ["DIMiddleware"]})
async def command_add_category(
    message: Message,
    finance_api_client: FinanceApiClient,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await AddCategoryHandler(finance_api_client).handle(message)
        logger.debug(f"The user #{user_id} executed the /add_category command.")
    except Exception as error:
        logger.exception(error)


@router.message(Command("get_categories"), flags={"middlewares": ["DIMiddleware"]})
async def command_get_categories(
    message: Message,
    finance_api_client: FinanceApiClient,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await GetCategoriesHandler(finance_api_client).handle(message)
        logger.debug(f"The user #{user_id} executed the /get_categories command.")
    except Exception as error:
        logger.exception(error)


@router.message(Command("help"), flags={"middlewares": ["DIMiddleware"]})
async def command_help(
    message: Message,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
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
