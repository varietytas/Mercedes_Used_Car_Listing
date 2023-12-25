from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


general_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Structure'),
    KeyboardButton('Overview'),
).add(
    KeyboardButton('Mean price over years')
)

exit_button = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Exit')
)
