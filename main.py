import asyncio

from aiogram import Dispatcher

from app.handler import router, bot, daily_send, daily_scheduler

dp = Dispatcher()
dp.include_router(router)

async def main():


    print("Бот включен")
    await dp.start_polling(bot)

# === Регистрация фоновой задачи ===
@dp.startup()
async def on_startup():
    asyncio.create_task(daily_scheduler(bot))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

"""функции бота :
   1. ежедневный парсинг  подобных данных
"Седмица 3-я по Пасхе. Глас 2.

Поста нет. 
Вмч. Георгия Победоносца (303). Иверской иконы Божией Матери (второе обретение списка иконы 2012).
Мц. царицы Александры (314). Мчч. Анатолия и Протолеона(303). Прп. Софии (1974). 
Сщмч. Иоанна пресвитера (1940).  конечно же сслыки на этих святых
 https://days.pravoslavie.ru/Days/20250216.html или https://azbyka.ru/days/ 
 
 2.расписание богослужений чтобы постил и закреплелял
 3. возможность отправить боту сообщение которое он запостит и закрепит"""
