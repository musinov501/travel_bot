from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db

def lang_buttons():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🇺🇿O'zbek", callback_data='uz')
    btn2 = InlineKeyboardButton("🇬🇧English", callback_data='en')
    btn3 = InlineKeyboardButton("🇷🇺Русский", callback_data='ru')
    markup.add(btn1, btn2, btn3)
    return markup


def travel_buttons(travels_list):
    markup = InlineKeyboardMarkup(row_width=2)
    for travel in travels_list:
        travel_id, travel_name = travel
        btn = InlineKeyboardButton(travel_name, callback_data=f'travel_{travel_id}')
        markup.add(btn)
    return markup



def travel_pagination_buttons(travel_id: int, page: int = 1):
    markup = InlineKeyboardMarkup()
    count = db.count_images(travel_id)[0]

    limit = 1
    offset = (page - 1) * limit

    image = db.select_image_by_pagination(travel_id, offset, limit)[1]

    previous = InlineKeyboardButton("⏮️ Previous", callback_data=f"prev_image_{travel_id}")
    current_page = InlineKeyboardButton(f"{page}/{count}", callback_data="current_page")
    next = InlineKeyboardButton("⏭️ Next", callback_data=f"next_image_{travel_id}")

    info = InlineKeyboardButton("ℹ️Info", callback_data=f"info_{travel_id}")
    back = InlineKeyboardButton("🔙Back", callback_data=f"back_to_{travel_id}")

    if page <= 1:
        markup.add(current_page, next)
    elif page >= count:
        markup.add(previous, current_page)
    else:
        markup.add(previous, current_page, next)
    markup.add(info)
    markup.add(back)

    return (image, markup)











