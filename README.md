# Travel Bot

**Travel Bot** is a Telegram bot designed to help users explore trips and famous sightseeing places. The bot supports multiple languages and provides interactive features such as viewing trips, pagination for images, and detailed sightseeing information.

---

## Features

- Multilingual support: Uzbek 🇺🇿, English 🇬🇧, Russian 🇷🇺
- User registration with name and phone number
- Browse available trips
- Paginated images for each trip
- View detailed info about trips (name, price, duration)
- Browse famous sightseeing places
- View images and descriptions of sightseeing places
- Location sharing

---

## Installation

```bash
1. Clone the repository:


git clone https://github.com/yourusername/travel-bot.git
cd travel-bot

2.  Install dependencies:

pip install -r requirements.txt

3. Set up your database:

# Run in Python shell
from data.loader import db
db.create_table_users()
db.create_table_travels()
db.create_table_images()
db.create_table_famous_places()

4.  Update your config.py with your Telegram bot token and other settings.

