from telebot import TeleBot
from config import TOKEN
from database.db import Database

bot = TeleBot(TOKEN)
db = Database()