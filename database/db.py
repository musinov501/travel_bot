import sqlite3

class Database:
    def __init__(self, db_name: str = 'main.db'):
        self.database = db_name


    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)

            result = None

            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()

            if commit:
                db.commit()

        return result

    #Registration part-> creating table of users
    def create_table_users(self):
            sql = '''CREATE TABLE IF NOT EXISTS users(
                telegram_id INTEGER NOT NULL UNIQUE,
                full_name TEXT,
                phone_number VARCHAR(13),
                lang VARCHAR(3)
                )'''
            self.execute(sql, commit=True)


    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?)'''
        self.execute(sql, telegram_id, commit=True)


    def  update_lang(self, lang, telegram_id):
        sql = '''UPDATE users SET lang = ? WHERE telegram_id = ?'''
        self.execute(sql, lang, telegram_id, commit=True)

    def get_user(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.execute(sql, telegram_id, fetchone=True)


    def get_lang(self, telegram_id):
        sql = '''SELECT lang FROM users WHERE telegram_id = ?'''
        result = self.execute(sql, telegram_id, fetchone=True)

        if result is None:
            return 'uz'
        return result[0]



    def save_phone_number_and_full_name(self, full_name, phone_number, telegram_id):
        sql =  '''UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, full_name, phone_number, telegram_id, commit=True)


    #Adding table of trips
    def create_table_travels(self):
        sql = '''CREATE TABLE IF NOT EXISTS travels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_uz TEXT,
            name_ru TEXT,
            name_en TEXT,
            price INTEGER,
            days INTEGER
            )
        '''
        self.execute(sql, commit=True)


    def drop_table_travels(self):
        sql = '''DROP TABLE IF EXISTS travels'''
        self.execute(sql, commit=True)

    def insert_travel(self, name_uz, name_ru, name_en, price, days):
        sql = '''INSERT INTO travels(name_uz, name_ru, name_en, price, days) VALUES (?, ?, ?, ?, ?) RETURNING id'''
        return self.execute(sql, name_uz, name_ru, name_en, price, days, commit=True, fetchone=True)[0]

    # Adding table of images
    def create_table_images(self):
        sql = '''CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            travel_id INTEGER REFERENCES travels(id)
            )
        '''
        self.execute(sql, commit=True)

    def insert_image(self, image: str, travel_id: int):
        sql = '''INSERT INTO images(image, travel_id) VALUES (?, ?)'''
        self.execute(sql, image, travel_id, commit=True)


    def count_images(self, travel_id):
        sql = '''SELECT count(id) FROM images WHERE travel_id = ?'''
        return self.execute(sql, travel_id, fetchone=True)


    def select_image_by_pagination(self, travel_id, offset, limit):
        sql = '''SELECT id, image FROM images WHERE travel_id = ? LIMIT ?, ?'''
        return self.execute(sql, travel_id, offset, limit, fetchone=True)



    def select_travels(self, lang):
        sql = f'''SELECT id, name_{lang} FROM travels'''
        return self.execute(sql, fetchall=True)


    def select_travel_text(self, travel_id, lang):
        sql = f'''SELECT name_{lang}, price, days FROM travels WHERE id = ?'''
        return self.execute(sql, travel_id, fetchone=True)


    def select_travels_with_images(self,travel_id, lang):
        sql = f'''SELECT  travels.id, travels.name_{lang}, images.id, images.image FROM travels JOIN images ON images.travel_id = travels.id WHERE travels.id = ?'''
        return self.execute(sql,travel_id, fetchall=True )


