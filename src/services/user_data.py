from telebot.types import User


def get_user_name(user_data: User) -> str:
    first_name = user_data.first_name
    last_name = user_data.last_name

    if first_name and not last_name:
        user_name = f"{first_name}"
    elif not first_name and last_name:
        user_name = f"{last_name}"
    elif not first_name and not last_name:
        user_name = "<user_name_empty>"
    else:
        user_name = f"{first_name} {last_name}"

    if user_data.is_premium:
        user_name = f"{user_name} ⭐"

    return user_name


def get_user_nick(user_data: User) -> str:
    user_nick = user_data.username

    if not user_nick:
        user_nick = "<user_name_empty>"
    else:
        user_nick = f"@{user_nick}"

    return user_nick


def get_user_link(user_data: User) -> str:
    user_link = user_data.username

    if not user_link:
        user_link = "#"
    else:
        user_link = f"https://t.me/{user_link}"

    return user_link
