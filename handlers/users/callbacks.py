from logging import makeLogRecord

from data.loader import bot, db
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from config import TEXTS
from keyboards.dafault import phone_button, make_buttons
from keyboards.inline import travel_buttons

REGISTER = {}


@bot.callback_query_handler(func=lambda call: call.data in ('uz', 'en', 'ru'))
def reaction_to_call(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = call.data
    db.update_lang(lang, from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    if None in db.get_user(from_user_id):
        text = TEXTS[lang][1]
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)
    else:
        text_buttons = TEXTS[lang][101]
        text = TEXTS[lang][5]
        bot.send_message(chat_id, text, reply_markup=make_buttons(text_buttons))


def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    if message.text:
        REGISTER[from_user_id] = {
            "full_name": message.text
        }
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)
    else:

        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)

    if message.contact:
        phone_number = message.contact.phone_number
        full_name = REGISTER[from_user_id]['full_name']
        db.save_phone_number_and_full_name(full_name, phone_number, from_user_id)

        names_buttons = TEXTS[lang][101]
        bot.send_message(chat_id, TEXTS[lang][3], reply_markup=make_buttons(names_buttons))

    else:
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)


@bot.callback_query_handler(func=lambda call: "travel_" in call.data)
def reaction_to_travel_(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    travel_id = int(call.data.split("_")[-1])
    lang= db.get_lang(from_user_id)
    print(db.select_travels_with_images(travel_id, lang))