from telebot import TeleBot
from telebot.types import Message
from storages import DataBaseSQLite3
from services import setting_logger, loading_arguments, get_user_name, get_user_link
from configs import ContainerWithStaticText as M, setting_bot

try:
    setting_logger()
    loading_arguments(setting_bot)
    db = DataBaseSQLite3()
except Exception as error:
    pass

bot = TeleBot(setting_bot.TOKEN)


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    chat_data = message.chat
    # user_message = message.text
    user_data = message.from_user
    user_name = get_user_name(user_data)
    user_link = get_user_link(user_data)
    bot.send_message(chat_data.id, M.HELLO % (user_link, user_name), parse_mode="html")


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    chat_data = message.chat
    # user_message = message.text
    user_data = message.from_user
    user_name = get_user_name(user_data)
    user_link = get_user_link(user_data)
    bot.send_message(chat_data.id, f"{M.HELLO % (user_link, user_name)}{M.LIST_COMMANDS}", parse_mode="html")


bot.polling(none_stop=True)  # or bot.infinity_polling()
