from aiogram.types import CallbackQuery, Message


def get_telegram_message_text(message: Message | CallbackQuery) -> str:
    if isinstance(message, Message):
        return message.text
    return message.message.text


def get_telegram_message_html_text(message: Message | CallbackQuery) -> str:
    if isinstance(message, Message):
        return message.html_text
    return message.message.html_text
