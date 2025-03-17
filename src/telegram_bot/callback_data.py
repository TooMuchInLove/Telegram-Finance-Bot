from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData


class ShowListButton(IntEnum):
    add_category = auto()
    get_categories = auto()
    get_wallets = auto()


class ShowMainButton(IntEnum):
    base = auto()
    delete = auto()
    update = auto()
    refresh = auto()
    back = auto()


class ShowListButtonCallbackData(CallbackData, prefix="main"):
    slug: ShowListButton


class ShowCategoriesCallbackData(CallbackData, prefix="categories"):
    slug: ShowMainButton
    name: str | None = None
    account_id: int | None = None
