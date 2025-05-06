from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):

     send_and_pin_text = State()


client = User()