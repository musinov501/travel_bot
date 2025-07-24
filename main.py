
from data.loader import bot, db
import handlers





if __name__ == '__main__':
    bot.remove_webhook()
    db.create_table_users()
    bot.infinity_polling()