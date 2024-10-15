from aiogram import Router

from telegram_bot.callback_handlers import router as handlers_router

router = Router(name=__name__)

router.include_routers(
    handlers_router,
)
