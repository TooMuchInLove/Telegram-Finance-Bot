from telebot.types import User


def get_user_name(user_data: User) -> str:
    first_name = user_data.first_name
    last_name = user_data.last_name
    is_premium = user_data.is_premium

    if first_name and not last_name:
        return f"{first_name}{_get_premium_status(is_premium)}"
    elif not first_name and last_name:
        return f"{last_name}{_get_premium_status(is_premium)}"
    elif not first_name and not last_name:
        return "<user_name_empty>"

    return f"{first_name} {last_name}{_get_premium_status(is_premium)}"


def get_user_nick(user_data: User) -> str:
    user_nick = user_data.username

    if not user_nick:
        return "<user_name_empty>"

    return f"@{user_nick}"


def get_user_link(user_data: User) -> str:
    user_link = user_data.username

    if not user_link:
        return "#"

    return f"https://t.me/{user_link}"


def _get_premium_status(is_premium: bool) -> str:
    if is_premium:
        return " ⭐"
    return ""
