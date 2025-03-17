from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from external_clients import FinanceApiClient, AddAccountHandler, DeleteCategoryHandler, GetCategoriesHandler
from telegram_bot.callback_data import (
    ShowListButton,
    ShowMainButton,
    ShowListButtonCallbackData,
    ShowCategoriesCallbackData,
)
from telegram_bot.states import StateAddCategory
from telegram_bot.utils import send_telegram_message, get_telegram_user_id

router = Router(name=__name__)


@router.callback_query(
    ShowCategoriesCallbackData.filter(F.slug == ShowMainButton.delete),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_categories_delete(
    query: CallbackQuery,
    finance_api_client: FinanceApiClient,
) -> None:
    await query.answer()
    user_id = get_telegram_user_id(query)
    logger.debug(f"The user #{user_id} clicked the 'delete' button for delete category.")
    await DeleteCategoryHandler(finance_api_client).handle(message=query)


@router.callback_query(
    ShowCategoriesCallbackData.filter(F.slug == ShowMainButton.refresh),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_categories_refresh(
    query: CallbackQuery,
    finance_api_client: FinanceApiClient,
) -> None:
    await query.answer()
    user_id = get_telegram_user_id(query)
    logger.debug(f"The user #{user_id} clicked the 'refresh' button.")
    await GetCategoriesHandler(finance_api_client).handle(message=query, is_update=True)


@router.callback_query(
    ShowCategoriesCallbackData.filter(F.slug == ShowMainButton.back),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_categories_back(
    query: CallbackQuery,
    finance_api_client: FinanceApiClient,
) -> None:
    await query.answer()
    user_id = get_telegram_user_id(query)
    logger.debug(f"The user #{user_id} clicked the 'back' button.")
    await AddAccountHandler(finance_api_client).handle(message=query, is_update=True)


@router.callback_query(
    ShowListButtonCallbackData.filter(F.slug == ShowListButton.add_category),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_add_categories(
    query: CallbackQuery,
    state: FSMContext,
    finance_api_client: FinanceApiClient,
) -> None:
    await query.answer()
    user_id = get_telegram_user_id(query)
    logger.debug(f"The user #{user_id} clicked the 'add_category' button.")
    # await GetCategoriesHandler(finance_api_client).handle(message=query, is_update=True)
    await state.set_state(StateAddCategory.info)
    # await state.update_data(info=query.data)
    await send_telegram_message(
        message=query,
        message_text="Enter the name of the category!",
        is_delete_message=True,
    )


@router.callback_query(
    ShowListButtonCallbackData.filter(F.slug == ShowListButton.get_categories),
    flags={"middlewares": ["DIMiddleware"]},
)
async def callback_get_categories(
    query: CallbackQuery,
    finance_api_client: FinanceApiClient,
) -> None:
    await query.answer()
    user_id = get_telegram_user_id(query)
    logger.debug(f"The user #{user_id} clicked the 'get_categories' button.")
    await GetCategoriesHandler(finance_api_client).handle(message=query, is_update=True)
