from aiogram.types import CallbackQuery, Message


def get_telegram_user_id(message: Message | CallbackQuery) -> int:
    if isinstance(message, Message):
        return message.from_user.id
    return message.message.chat.id


def get_telegram_user_name(message: Message) -> str:
    user = message.from_user
    first_name = user.first_name
    last_name = user.last_name
    is_premium = user.is_premium

    if first_name and not last_name:
        return f"{first_name}{_get_premium_status(is_premium)}"
    elif not first_name and last_name:
        return f"{last_name}{_get_premium_status(is_premium)}"
    elif not first_name and not last_name:
        return "<user_name_empty>"

    return f"{first_name} {last_name}{_get_premium_status(is_premium)}"


def get_telegram_user_nick(message: Message) -> str:
    user_nick = message.from_user.username

    if not user_nick:
        return "<user_name_empty>"

    return user_nick


def get_telegram_user_link(message: Message) -> str:
    user_link = message.from_user.username

    if not user_link:
        return "#"

    return f"https://t.me/{user_link}"


def get_the_entered_words(message: Message) -> list[str]:
    return message.text.split()


def _get_premium_status(is_premium: bool) -> str:
    if is_premium:
        return " ⭐"
    return ""
