from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.callback_data import (
    ShowListButton,
    ShowMainButton,
    ShowListButtonCallbackData,
    ShowCategoriesCallbackData,
)


def get_inline_buttons_for_main_list() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="1. Add category",
                callback_data=ShowListButtonCallbackData(slug=ShowListButton.add_category).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="2. Get categories",
                callback_data=ShowListButtonCallbackData(slug=ShowListButton.get_categories).pack()
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_inline_buttons_for_categories(data: list[list[dict[str, Any]]] | None = None) -> InlineKeyboardMarkup | None:
    buttons = []

    if data:
        for line in data:
            inline_buttons = [
                InlineKeyboardButton(
                    text="✏️",
                    callback_data=ShowCategoriesCallbackData(
                        slug=ShowMainButton.update,
                        name=line[0]["name"],
                        account_id=line[0]["account_id"],
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="❌",
                    callback_data=ShowCategoriesCallbackData(
                        slug=ShowMainButton.delete,
                        name=line[1]["name"],
                        account_id=line[1]["account_id"],
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=line[2]["name"],
                    callback_data=ShowCategoriesCallbackData(
                        slug=ShowMainButton.base,
                        name=line[2]["name"],
                        account_id=line[2]["account_id"],
                    ).pack(),
                ),
            ]
            buttons.append(inline_buttons)

    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙BACK",
                callback_data=ShowCategoriesCallbackData(slug=ShowMainButton.back).pack(),
            ),
            InlineKeyboardButton(
                text="♻️REFRESH",
                callback_data=ShowCategoriesCallbackData(slug=ShowMainButton.refresh).pack(),
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
