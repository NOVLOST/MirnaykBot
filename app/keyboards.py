from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton,InlineKeyboardMarkup)


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Расписание на богослужений на эту неделю 📝")

        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)



