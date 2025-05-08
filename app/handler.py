import os
import datetime
import asyncio

from aiogram import F, Router,Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

import app.keyboards as kb
import classes.client_class as cl

LAST_TIME_FILE = "timesend.txt"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
CHAT_ID = "-1001603940184"

router = Router()
bot = Bot(token='7662881278:AAGGFZ3tj7rC4DxOvfXlp51Qho5aeWC4uJ0')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Здравствуйте!мои команды:\n"
                         "1./sendandpin - команда для закрепления и отправки  сообщения в чат\n"
                         ,reply_markup=kb.start_keyboard)

@router.message(F.text == "Расписание на богослужений на эту неделю 📝")
async def cmd_timetable(message: Message):
    photo = FSInputFile("timetable.jpg")
    now = datetime.datetime.now().day
    print(now)
    await bot.send_photo(chat_id="-1001603940184", photo=photo)

@router.message(F.text == "/sendandpin")
async def cmd_sendandpin(message: Message,state: FSMContext):
    await state.set_state(cl.client.send_and_pin_text)
    await message.answer("отправте любое сообщение и я его закреплю в чате.")


@router.message(cl.client.send_and_pin_text)
async def sendandpin_mod(message: Message,state: FSMContext):
    await state.update_data(send_and_pin_text = message.text)
    data = await state.get_data()
    sent_message = await bot.send_message(
        chat_id="-1001603940184",
        text=data["send_and_pin_text"],
        parse_mode="HTML"
    )

    await bot.pin_chat_message(
        chat_id= "-1001603940184",
        message_id=sent_message.message_id
    )

async def daily_send(bot: Bot, chat_id:str):

    now_day = datetime.datetime.now().day
    last_send_day = load_last_time(LAST_TIME_FILE)

    if now_day != last_send_day :

        await bot.send_message(chat_id = "-1001603940184" , text = "its me!!!" )
        print("aaaaaa")
        save_last_time(now_day,LAST_TIME_FILE)

def load_last_time(file_name):
    with open(file_name,"r") as file:

        return file.read()

async def daily_scheduler(bot: Bot):
    while True:
        await daily_send(bot, CHAT_ID)
        await asyncio.sleep(60*60)  # Проверяем каждые 60 минут

def save_last_time(now_day,file_name):
    with open(file_name,"w") as file:

        return file.write(str(now_day))
