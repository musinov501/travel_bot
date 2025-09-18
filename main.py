
from data.loader import bot, db
import handlers





if __name__ == '__main__':

    db.create_table_users()
    # db.drop_table_travels()
    db.create_table_travels()
    db.create_table_images()
    db.create_table_famous_places()
    db.create_table_excursions()
    bot.remove_webhook()
    bot.infinity_polling()