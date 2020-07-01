"""Удаление счета из профиля пользователя"""

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from data.config import YES_CHOICES, NO_CHOICES
from handlers.users.menu import get_markup_main, get_accounts_markup
from keyboards.default.menu import markup_cancel, markup_yes_cancel, markup_yes_no_cancel
from loader import dp
from states.states import RemoveForm
from utils.db_api.models import Profile, Account
from utils.db_api.models import get_or_create, session_class, commit_session, get_account_from_profile, remove_account
from utils.site.parsing import get_address


@dp.message_handler(commands='remove')
@dp.message_handler(Text(equals=['удалить', 'remove'], ignore_case=True), state='*')
async def process_remove(message: Message, state: FSMContext):
    """
    Выбор счета для удаления
    """
    # Set state
    await RemoveForm.choice_account.set()
    reply_markup = get_accounts_markup(message.from_user.id)
    await message.answer('Выберите лицевой счет для удаления', reply_markup=reply_markup)


@dp.message_handler(lambda message: message.text.isdigit(), state=RemoveForm.choice_account)
async def confirm_account(message: Message, state: FSMContext):
    await RemoveForm.next()
    acc_for_delete = get_account_from_profile(user_id=message.from_user.id, account=message.text)

    if not acc_for_delete:
        await state.finish()
        await message.answer('Нет такого счета', reply_markup=get_markup_main)
    await state.update_data(choice_account=message.text)
    await message.answer(f'Счет: {message.text}\n'
                         f'Адрес: {acc_for_delete.address}\n'
                         f'Удалить?', reply_markup=markup_yes_cancel)


@dp.message_handler(Text(equals=YES_CHOICES, ignore_case=True), state=RemoveForm.confirm)
async def process_address_confirm(message: Message, state: FSMContext):
    """
    Обработка подтверждения удаления счета
    """
    async with state.proxy() as data:
        data['confirm'] = True
        result = remove_account(user_id=message.from_user.id, account=data['choice_account'])
        answer_text = 'Счет удален' if result else 'Нет такого счета'
        await message.answer(answer_text, reply_markup=get_markup_main(message.from_user.id))
    await state.finish()