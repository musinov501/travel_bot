from data.loader import bot
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data in ('uz', 'en', 'ru'))
def reaction_to_call(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    print(call.data)