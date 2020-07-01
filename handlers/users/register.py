from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from data.config import YES_CHOICES, NO_CHOICES
from handlers.users.menu import get_markup_main
from keyboards.default.menu import markup_cancel, markup_yes_no_cancel
from loader import dp
from states.states import Register
from utils.db_api.models import Profile, get_or_create, Account, session_class, commit_session
from utils.site.parsing import get_address


@dp.message_handler(commands='register')
@dp.message_handler(Text(equals=['регистрация'], ignore_case=True), state='*')
async def process_start_register(message: Message):
    """Начало регистрации"""
    # Set state
    await Register.account.set()
    await message.answer('Зарегистрировавшись в Telegram канале вы получите возможность автоматически получать '
                         'уведомления о предстоящих отключениях.\n'
                         'Введите персональный счет (37ХХХХХХ)', reply_markup=markup_cancel)


# Проверка счета. Только цифры
@dp.message_handler(lambda message: not message.text.isdigit(), state=Register.account)
@dp.message_handler(lambda message: len(message.text) != 8, state=Register.account)
async def process_account_invalid(message: Message):
    """Если формат счета не верен"""
    return await message.reply('Счет должен быть только из цифр.\n'
                               'Введите персональный счет (37ХХХХХХ)',
                               reply_markup=markup_cancel)


@dp.message_handler(lambda message: message.text.isdigit(), state=Register.account)
async def process_account(message: Message, state: FSMContext):
    # Update state and data
    await Register.address_confirm.set()
    await state.update_data(account=message.text)
    address = get_address(message.text)
    if address:
        await state.update_data(address=address)
        await message.answer(f' {address}\n'
                             f'Адрес верен?', reply_markup=markup_yes_no_cancel)
    else:
        await message.answer('Адрес не найден.\n'
                             'Все равно подтвердить?', reply_markup=markup_yes_no_cancel)


@dp.message_handler(lambda message: message.text.lower() not in (YES_CHOICES + NO_CHOICES),
                    state=Register.address_confirm)
async def process_address_confirm_invalid(message: Message):
    """Обработка ошибки подтверждения адреса"""
    return await message.reply('Не понял ответ.\n'
                               'Адрес верен? Выберите на клавиатуре.')


@dp.message_handler(Text(equals=NO_CHOICES, ignore_case=True), state=Register.address_confirm)
async def process_address_confirm_no(message: Message):
    """Обработка подтверждения адреса c ответом НЕТ"""
    await Register.account.set()
    await message.reply('Введите счет. (только цифры)', reply_markup=markup_cancel)


@dp.message_handler(Text(equals=YES_CHOICES, ignore_case=True), state=Register.address_confirm)
async def process_address_confirm(message: Message, state: FSMContext):
    """Обработка подтверждения адреса"""
    async with state.proxy() as data:
        data['address_confirm'] = True

        session = session_class()

        profile, created = get_or_create(
            session,
            Profile,
            external_id=message.from_user.id,
            name=message.from_user.username,
        )
        account, created = get_or_create(
            session,
            Account,
            profile=profile,
            account=data['account'],
        )
        if account:
            answer_text = 'Счет зарегистрирован' if created else 'Такой счет уже зарегистрирован'
            account.address = data['address']
            commit_session(session)
        else:
            answer_text = 'Ошибка!'
        await message.answer(answer_text, reply_markup=get_markup_main(message.from_user.id))

    # Finish conversation
    await state.finish()
