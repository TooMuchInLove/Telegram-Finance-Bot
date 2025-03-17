from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from src.external_clients import (
    FinanceApiClient,
    AddAccountHandler,
    AddCategoryHandler,
)
from src.telegram_bot.states import StateAddCategory
from src.telegram_bot.utils import get_telegram_user_id

router = Router(name=__name__)


@router.message(CommandStart(), flags={"middlewares": ["DIMiddleware"]})
async def command_start(message: Message, finance_api_client: FinanceApiClient) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await AddAccountHandler(finance_api_client).handle(message=message)
        logger.debug(f"The user #{user_id} executed the /start command.")
    except Exception as error:
        logger.exception(error)


@router.message(Command("add_category"), flags={"middlewares": ["DIMiddleware"]})
async def command_add_category(message: Message, finance_api_client: FinanceApiClient) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await AddCategoryHandler(finance_api_client).handle(message=message)
        logger.debug(f"The user #{user_id} executed the /add_category command.")
    except Exception as error:
        logger.exception(error)


@router.message(StateAddCategory.info, F.text, flags={"middlewares": ["DIMiddleware"]})
async def state_command_add_category(
    message: Message,
    state: FSMContext,
    finance_api_client: FinanceApiClient,
) -> None:
    try:
        user_id = get_telegram_user_id(message)
        await AddCategoryHandler(finance_api_client).handle(message=message)
        logger.debug(f"The user #{user_id} executed the /add_category command.")
        await state.clear()
    except Exception as error:
        logger.exception(error)


@router.message(Command("help"), flags={"middlewares": ["DIMiddleware"]})
async def command_help(message: Message) -> None:
    try:
        user_id = get_telegram_user_id(message)
        logger.debug(f"The user #{user_id} executed the /help command.")
    except Exception as error:
        logger.exception(error)


@router.message(F.text, flags={"middlewares": ["DIMiddleware"]})
async def custom_text(message: Message) -> None:
    try:
        user_id = get_telegram_user_id(message)
        logger.debug(f"The user #{user_id} entered a message.")
    except Exception as error:
        logger.exception(error)
