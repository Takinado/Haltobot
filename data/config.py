import os

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
RANGE_DAYS_FOR_SEARCH_ADDRESS = (-48*7, 4*7)
