
from data.loader import bot, db
import handlers





if __name__ == '__main__':

    db.create_table_users()
    # db.drop_table_travels()
    db.create_table_travels()
    db.create_table_images()
    db.create_table_famous_places()
<<<<<<< HEAD
    db.create_table_excursions()
=======
>>>>>>> 2ad76f62c3b291b7635edc9cb8248f41500a48c8
    bot.remove_webhook()
    bot.infinity_polling()