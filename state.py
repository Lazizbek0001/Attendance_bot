from aiogram.dispatcher.filters.state import State, StatesGroup

class UserDate(StatesGroup):
    photo = State()
    check = State()
    