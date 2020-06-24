"""Configure ReplyKeyboardMarkup"""
from aiogram.types import ReplyKeyboardMarkup

CANCEL = 'Отмена'

markup_main = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_main.add('Регистрация')

markup_main_login = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_main_login.add('Регистрация', 'Удалить')

markup_cancel = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_cancel.add(CANCEL)

markup_cancel_login = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_cancel_login.add(CANCEL, 'Удалить')

markup_yes_no_cancel = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_yes_no_cancel.add('Да', 'Нет', CANCEL)

markup_yes_cancel = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
markup_yes_cancel.add('Да', CANCEL)
