from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    account = State()
    address = State()
    address_confirm = State()


class RemoveForm(StatesGroup):
    choice_account = State()
    confirm = State()
