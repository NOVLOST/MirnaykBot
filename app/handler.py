import datetime
import asyncio

from aiogram import F, Router,Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,CallbackQuery,ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import requests as re
from bs4 import BeautifulSoup as bs

import app.keyboards as kb
import classes.client_class as cl

#NOTE: сделать str() на if иначе не будет проверка на день работать верно
#TODO: доделать гиперссылки в сообщение
LAST_TIME_FILE = "timesend.txt"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
CHAT_ID = "-1001603940184"

router = Router()
bot = Bot(token='7662881278:AAGGFZ3tj7rC4DxOvfXlp51Qho5aeWC4uJ0')
HEADER = {"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Здравствуйте!мои команды:\n"
                         "1./sendandpin - команда для закрепления и отправки  сообщения в чат\n"
                         ,reply_markup=kb.start_keyboard)

@router.message(F.text == "Расписание на богослужений на эту неделю 📝")
async def cmd_timetable(message: Message):
    photo = FSInputFile("timetable.jpg")
    now = datetime.date.today()
    print(now - datetime.timedelta(days = 13))
    await message.answer_photo(photo=photo)
    

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
#-----------------------------
#парсинг и расслыка сообщений
#-----------------------------
async def daily_send(bot: Bot, chat_id:str):

    today_date = datetime.date.today() #берем сегоднящнюю дату
    last_send_day = load_last_time(LAST_TIME_FILE) #берем дату прошлой отправки
    print(type(today_date.day),type(last_send_day))

    if today_date.day != last_send_day :

        old_style_date = str((today_date - datetime.timedelta(days = 13))).replace("-","") #перевод на старый стиль
        message_str = '' #будущее сообщение
        url = f"https://days.pravoslavie.ru/Days/{old_style_date}.html"
        response = re.get(url,headers=HEADER)

        soup = bs(response.text, "lxml")

        #какой день пост/непост
        data = soup.find("table" ,style="border-collapse: collapse")
        span_teg = data.find_all("span")
        for teg in span_teg:
            message_str += teg.text
        message_str += "\n\n"
        print(span_teg)
        #кого поминаем
        data = soup.find("div",class_="DD_TEXT")
        span_teg = data.find_all("span") #в спане лежат теги а которые хранят имена

        links = []
        a_teg_name = []
        for teg in span_teg:
            a_teg = teg.find('a',title=True)
            a_teg_name.append(a_teg['title'])
            links.append(a_teg.get('href'))

        print(links)
        print(a_teg_name)

        for teg,link in zip(a_teg_name,links): #формируем гиперссылки

            markdown_link = f'<a href="{link}">{teg}</a> \n'
            message_str += markdown_link
        message_str += "\n\n"
        print(span_teg,"P_TEG")
        #феофан на каждый день
        data = soup.find("p",class_="DP_FEOF")
        message_str += data.text

        await bot.send_message(chat_id = "-1001603940184" , text = message_str,parse_mode='HTML' )
        save_last_time(today_date.day,LAST_TIME_FILE)

def load_last_time(file_name): #загрузка последнего времени отправки
    with open(file_name,"r") as file:

        return file.read()

async def daily_scheduler(bot: Bot): #цикл отправки сообщения
    while True:
        await daily_send(bot, CHAT_ID)
        await asyncio.sleep(60*60)  # Проверяем каждые 60 минут

def save_last_time(now_day,file_name):#сохранения последенего времени отправки
    with open(file_name,"w") as file:

        return file.write(str(now_day))
