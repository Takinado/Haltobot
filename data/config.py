import os
from urllib.parse import urljoin

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
admins = [
]

ip = os.getenv('ip')

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

YES_CHOICES = ['yes', 'y', 'да', 'д']
NO_CHOICES = ['no', 'n', 'нет', 'н']
CANCEL_CHOICES = ['cancel', 'отмена']

# Test account
TEST_DATA = os.getenv('TEST_DATA')

# Heroku need srt
DAYS_AHEAD_FOR_SEARCH = int(os.getenv('DAYS_AHEAD_FOR_SEARCH', '3'))
# NOTIF_PERIOD = '60*60*24'
NOTIF_PERIOD = int(os.environ.get('NOTIF_PERIOD', '60'))
RANGE_DAYS_FOR_SEARCH_ADDRESS = (-48*7, 4*7)


DB_USER = str(os.getenv('DB_USER'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST', 'localhost'))
DB_PORT = str(os.getenv('DB_PORT', '5432'))
DB_NAME = str(os.getenv('DB_NAME'))

PROJECT_NAME = 'haltobot-bot'

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com/'  # Enter here your link from Heroku project settings
WEBHOOK_URL_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)

WEBAPP_HOST = '0.0.0.0'  # Слушаем все подключения к нашему приложению
WEBAPP_PORT = os.environ.get('PORT', '5000')
