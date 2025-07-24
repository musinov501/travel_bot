from telebot.types import Message
from data.loader import bot, db
from keyboards.inline import lang_buttons

@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not db.get_user(from_user_id):
        db.insert_telegram_id(from_user_id)
        text = (f"🇺🇿Assalomu alaykum ✈️Travello tur agentligiga xush kelibsiz!!!\n"
                f"Iltimos tilni tanglang!!!\n\n"
                f"🇬🇧Hello, welcome to ✈️Travello tour agency!!!\nPlease select the language!!!\n\n"
                f"🇷🇺Здравствуйте, добро пожаловать в туристическое агентство ✈️Travello!!!\nПожалуйста, выберите язык!!!")
        bot.send_message(chat_id, text, reply_markup=lang_buttons())

    else:
        bot.send_message(chat_id, "Ro'yxatdan o'tgansiz")


