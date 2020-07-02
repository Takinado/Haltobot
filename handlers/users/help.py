from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from handlers.users.menu import get_markup_main
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    """Отправляет помощь по боту"""
    text = [
        'Список команд: ',
        '/start - Начать',
        '/help - Получить справку',
        '/register - Регистрация',
        '/now - Получить данные по отключениям сейчас',
    ]
    await message.answer('\n'.join(text), reply_markup=get_markup_main(message.from_user.id))
