from asyncio import sleep as asyncio_sleep

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from configs import setting_bot


async def send_telegram_message(
    message: Message | CallbackQuery,
    message_text: str,
    is_update_text: bool = False,
    buttons: InlineKeyboardMarkup | None = None,
    is_delete_message: bool = False,
    is_disable_web_page_preview: bool = True,
) -> None:

    if isinstance(message, CallbackQuery):
        message = message.message

    if buttons is None:
        if is_update_text:
            msg = await message.edit_text(
                text=message_text,
                disable_web_page_preview=is_disable_web_page_preview,
            )
        else:
            msg = await message.answer(
                text=message_text,
                disable_web_page_preview=is_disable_web_page_preview,
            )
    else:
        if is_update_text:
            msg = await message.edit_text(
                text=message_text,
                reply_markup=buttons,
                disable_web_page_preview=is_disable_web_page_preview,
            )
        else:
            msg = await message.answer(
                text=message_text,
                reply_markup=buttons,
                disable_web_page_preview=is_disable_web_page_preview,
            )

    if is_delete_message:
        await asyncio_sleep(setting_bot.TIMEOUT_DELETE_MESSAGE)
        await msg.delete()
