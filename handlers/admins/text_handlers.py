from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db

from keyboards.dafault import make_buttons
from config import ADMINS, TEXTS



admin_buttons_names = [
        "➕ Sayohatlar qo'shish",
        "➕ Mashxur joylar qo'shish",
        "➕ Ekskursiya jadvali"
    ]


TRAVEL = {}


@bot.message_handler(func=lambda message: message.text == "👮🏻‍♂️Admin buyruqlari")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Admin buyruqlari", reply_markup=make_buttons(admin_buttons_names, back=True))



@bot.message_handler(func=lambda message: message.text == "➕ Sayohatlar qo'shish")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Sayohat nomini o'zbek tilida kiriting", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_uz_travel)


def get_name_uz_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "name_uz": message.text
    }

    msg = bot.send_message(chat_id, "Sayohat nomini rus tilida kiriting")
    bot.register_next_step_handler(msg, get_name_ru_travel)



def get_name_ru_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    TRAVEL[from_user_id]['name_ru'] = message.text
    msg = bot.send_message(chat_id, "Sayohat nomini ingliz tilida kiriting")
    bot.register_next_step_handler(msg, get_name_en_travel)

def get_name_en_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['name_en'] = message.text
    msg = bot.send_message(chat_id, "Sayohat narxini kiriting")
    bot.register_next_step_handler(msg, get_price_travel)




def get_price_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['price'] = message.text
    msg = bot.send_message(chat_id, "Sayohat davomiyligini kiriting")
    bot.register_next_step_handler(msg, get_days_travel)


def get_days_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['days'] = message.text
    msg = bot.send_message(chat_id, "Sayohat rasmi linkini yuboring")
    bot.register_next_step_handler(msg, get_image_travel)



def get_image_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not TRAVEL[from_user_id].get('images'):
        TRAVEL[from_user_id]['images'] = [message.text]
    else:
        TRAVEL[from_user_id]['images'].append(message.text)
    msg = bot.send_message(chat_id, "Yana rasm qo'shasizmi?",
                           reply_markup=make_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_travel)





def save_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == 'No':

        name_uz = TRAVEL[from_user_id]['name_uz']
        name_ru = TRAVEL[from_user_id]['name_ru']
        name_en = TRAVEL[from_user_id]['name_en']
        price = int(TRAVEL[from_user_id]['price'])
        days = int(TRAVEL[from_user_id]['days'])
        images = TRAVEL[from_user_id]['images']
        travel_id = db.insert_travel(name_uz, name_ru, name_en, price, days)
        del TRAVEL[from_user_id]
        for image in images:
            db.insert_image(image, travel_id)

        bot.send_message(chat_id, "Sayohat saqlandi!!",
                         reply_markup=make_buttons(admin_buttons_names, back=True))
    else:
        msg = bot.send_message(chat_id, "Sayohat rasmi linkini yuboring", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_image_travel)


@bot.message_handler(regexp="⬅️Ortga")
def reaction_to_back(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    names_buttons = TEXTS[lang][101]
    bot.send_message(chat_id, TEXTS[lang][4], reply_markup=make_buttons(names_buttons, admin_id=from_user_id))

