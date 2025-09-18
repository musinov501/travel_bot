from telebot.types import Message
from data.loader import bot, db
from config import TEXTS
from keyboards.dafault import make_buttons
<<<<<<< HEAD
from keyboards.inline import lang_buttons, travel_buttons, famous_places_buttons, excursions_buttons
=======
from keyboards.inline import lang_buttons, travel_buttons, famous_places_buttons
>>>>>>> 2ad76f62c3b291b7635edc9cb8248f41500a48c8
from .callbacks import get_name




@bot.message_handler(func= lambda message:  message.text in TEXTS[db.get_lang(message.from_user.id)][101])
def reaction_to_packages(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    if message.text in ["⚙️Settings", "⚙️Настройки", "⚙️Sozlamalar"]:
        btn_texts = TEXTS[lang][102]
        text = TEXTS[lang][6]
        msg = bot.send_message(chat_id, text, reply_markup=make_buttons(btn_texts, lang = lang, back = True))
        bot.register_next_step_handler(msg, get_settings)
    elif message.text == TEXTS[lang][101][0]:
        travels_list = db.select_travels(lang)
        text = TEXTS[lang][8]
        bot.send_message(chat_id, text , reply_markup=travel_buttons(travels_list))
<<<<<<< HEAD
        
        
    elif message.text == TEXTS[lang][101][1]:
        places = db.select_famous_places(lang)
        markup = famous_places_buttons(places)
        text = "Mashhur joylarni tanlang 👇👇"
        bot.send_message(chat_id, text, reply_markup=markup)
        
    elif message.text == TEXTS[lang][101][2]:
        excursions = db.select_excursions(lang)
        markup = excursions_buttons(excursions)
        text = "Ekskursiyalarni tanlang 👇👇"
        bot.send_message(chat_id, text, reply_markup=markup)
=======
    elif message.text == TEXTS[lang][101][1]:
        markup = famous_places_buttons(lang)
        bot.send_message(chat_id, "🏛 Mashhur joylarni tanlang:", reply_markup=markup)
        
>>>>>>> 2ad76f62c3b291b7635edc9cb8248f41500a48c8
    elif message.text == TEXTS[lang][101][5]:
        msg = bot.send_message(chat_id, "Loc yuboring")
        bot.register_next_step_handler(msg, get_location)





def get_settings(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)

    if message.text in ["⬅️Назад", "⬅️Back", "⬅️Ortga", "/start"]:
        btn_names = TEXTS[lang][101]
        text = TEXTS[lang][4]
        bot.send_message(chat_id, text,reply_markup=make_buttons(btn_names))

    else:
        if message.text == TEXTS[lang][102][0]:
            text = TEXTS[lang][7]
            bot.send_message(chat_id, text, reply_markup=lang_buttons())




@bot.message_handler(func=lambda message: message.text == TEXTS[db.get_lang(message.from_user.id)][102][1])
def reaction_to_re_registration(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, get_name)



@bot.message_handler(content_types=['location'])
def get_location(message: Message):
    chat_id = message.chat.id
    lat = message.location.latitude
    long = message.location.longitude
    bot.send_location(chat_id, lat, long)



