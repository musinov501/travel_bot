from telebot.types import Message
from data.loader import bot, db
from config import TEXTS
from keyboards.dafault import make_buttons
from keyboards.inline import lang_buttons, travel_buttons, famous_places_buttons, excursions_buttons
from .callbacks import get_name
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton




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
    elif message.text == TEXTS[lang][101][3]:
        guide = db.select_guide_by_excursion(1)  # for now, just test with excursion_id=1
        
        if guide:
            full_name, phone, tg_username = guide[1], guide[2], guide[3]
            
            text = f"👨‍💼 Guide: {full_name}\n📞 Phone: {phone}\n✈️ Telegram: @{tg_username}"
            
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("💬 Contact on Telegram", url=f"https://t.me/{tg_username}")
            )
            
            bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "No guide available yet ❌")
    
    
    elif message.text == TEXTS[lang][101][4]:
        travels = db.select_travels(lang)
        excursions = db.select_excursions(lang)
        
        
        text = "Narxlarni qaysi kategoriya bo'yicha ko'rmoqchisiz? 👇"
        markup = InlineKeyboardMarkup()
        
        
        for t in travels:
            markup.add(
                InlineKeyboardButton(f"✈️ {t[1]}", callback_data=f"price_travel_{t[0]}")
                )
            
        for e in excursions:
            markup.add(
                InlineKeyboardButton(f"🗺 {e[1]}", callback_data=f"price_excursion_{e[0]}")
            )
            
        bot.send_message(chat_id, text, reply_markup=markup)
        
    
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



