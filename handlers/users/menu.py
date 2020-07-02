import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from data.config import CANCEL_CHOICES, TEST_DATA
from loader import dp
from aiogram.types import Message, ReplyKeyboardMarkup
from keyboards.default.menu import (
    markup_main,
    markup_cancel,
    markup_main_login,
    markup_cancel_login,
)
from utils.db_api.models import session_class, Account, get_accounts_to_sending
from utils.site.parsing import get_data


def get_markup_main(user_id):
    reply_markup = markup_main
    session = session_class()
    if session.query(Account).join(Account.profile, aliased=True).filter_by(external_id=user_id).first():
        reply_markup = markup_main_login
    return reply_markup


def get_markup_cancel(user_id):
    reply_markup = markup_cancel
    session = session_class()
    if session.query(Account).join(Account.profile, aliased=True).filter_by(external_id=user_id).first():
        reply_markup = markup_cancel_login
    return reply_markup


def get_accounts_markup(from_user_id):
    accounts_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    session = session_class()
    accounts = session.query(Account).join(Account.profile, aliased=True).filter_by(external_id=from_user_id)
    for account in accounts:
        accounts_markup.add(account.account)
    accounts_markup.add("Отмена")
    return accounts_markup


@dp.message_handler(CommandStart())
async def send_welcome(message: Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    text = [
        'Бот для получения уведомлений об отключениях электричества в Херсонской области Украины.\n',
        '/start - Начать',
        '/help - Получить справку',
        '/register - Регистрация',
        '/new - Получить данные по отключения сейчас',

    ]
    await message.answer('\n'.join(text), reply_markup=get_markup_main(message.from_user.id))


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals=CANCEL_CHOICES, ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Разрешает пользователю отменить любое действие
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.answer('Отменено.', reply_markup=get_markup_main(message.from_user.id))


@dp.message_handler(Text(equals=CANCEL_CHOICES, ignore_case=True))
async def cancel_to_start_handler(message: Message, state: FSMContext):
    """
    Разрешает пользователю отменить все и перейти в начало
    """
    await message.answer('Отменено.', reply_markup=get_markup_main(message.from_user.id))


@dp.message_handler(commands='test')
async def test(message: Message, state: FSMContext):
    records = get_data(TEST_DATA)
    if records:
        for record in records:
            await message.answer(f"{record['date']} {record['time']}\n{record['comment']}")
    else:
        await message.answer('Нет данных')


@dp.message_handler(commands='now')
async def now(message: Message, state: FSMContext):
    """Получить данные по зарегистрированным счетам прямо сейчас"""
    accounts = get_accounts_to_sending(message.from_user.id)
    for account in accounts:
        records = get_data(account.account)
        if records:
            for record in records:
                await message.answer(f"{record['date']} {record['time']}\n{account.address}\n{record['comment']}")
        else:
            await message.answer('Нет данных')
