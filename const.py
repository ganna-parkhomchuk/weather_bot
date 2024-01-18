"""
This module contains configuration settings and constants for a Weather Telegram Bot.
"""

TOKEN = '6460151196:AAGxjBGqOQboFwVPEOcqf3wL2s8vK0UKVdE'

URL = 'https://api.telegram.org/bot{token}/{method}'

UPDATE_METHOD = 'getUpdates'
SEND_METHOD = 'sendMessage'

MY_ID = 5831882021

UPDATE_ID_FILE_PATH = 'update_id'

with open(UPDATE_ID_FILE_PATH) as file:
    data = file.readline()
    if data:
        data = int(data)
    UPDATE_ID = data


WEATHER_TOKEN = 'dddc04a6919f7f064b6cf3745919b25e'

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}'


