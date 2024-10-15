from dataclasses import dataclass

from configs import setting_bot


# TODO: по хорошему переделать на систему шаблнов (например, jinja2)

@dataclass(slots=True, frozen=True)
class ContainerWithStaticText:
    # ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ
    HELLO = f"Привет, <b><a href='%s'>%s</a></b>\nЯ бот @{setting_bot.NAME}\n"
    # СПИСОК КОМАНД БОТА
    LIST_COMMANDS = (
        "\n<b>Посмотрите список моих команд</b>:\n"
        "1. Начало работы: /start\n"
        "2. Посмотреть список текущих категорий: /get_categories\n"
        "3. Посмотреть состояние счетов: /account\n"
        "4. Посмотреть расходы за день/месяц: /day_expenses /monthly_expenses\n"
        "5. Посмотреть доходы за день/месяц: /daily_income /monthly_income\n"
        "6. Введите расходы: /add_expenses\n"
        "7. Введите доходы: /add_income\n"
    )


@dataclass(slots=True)
class LogBot:
    SUCCESS_START = "Starting..."
    SUCCESS_STOP = "Stopping..."
    WARNING_DISABLE = "The bot is disabled."
