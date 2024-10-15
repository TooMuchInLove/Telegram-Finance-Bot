from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_menu(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="start",
                description="🚀 Start",
            ),
            BotCommand(
                command="help",
                description="❔ Help",
            ),
        ],
        scope=BotCommandScopeDefault(),
    )
