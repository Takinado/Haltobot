import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from data.config import CANCEL_CHOICES, TEST_DATA
from loader import dp
from aiogram.types import Message
from keyboards.default.menu import markup_main, markup_cancel
from utils.site.parsing import get_data


def get_markup_main(user_id):
    reply_markup = markup_main
    # if Account.objects.filter(profile__external_id=user_id).first():
    #     reply_markup = markup_main_login
    # else:
    #     reply_markup = markup_main
    return reply_markup


def get_markup_cancel(user_id):
    reply_markup = markup_cancel
    # if Account.objects.filter(profile__external_id=user_id).first():
    #     reply_markup = markup_cancel_login
    # else:
    #     reply_markup = markup_cancel
    return reply_markup


@dp.message_handler(CommandStart())
async def send_welcome(message: Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    text = [
        'Бот для получения уведомлений об отключениях электричества в Херсонской области Украины.\n',
        '/start - Начать',
        '/help - Получить справку',
        '/register - Регистрация',
    ]
    await message.answer('\n'.join(text), reply_markup=get_markup_main(message.from_user.id))


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals=CANCEL_CHOICES, ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Разрешает пользователь отменить любое действие
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.answer('Отменено.', reply_markup=get_markup_main(message.from_user.id))


@dp.message_handler(commands='test')
async def test(message: Message, state: FSMContext):
    records = get_data(TEST_DATA)
    if records:
        for record in records:
            await message.answer(' '.join([record['date'], record['time'], record['comment']]))
    else:
        await message.answer('Нет данных')
