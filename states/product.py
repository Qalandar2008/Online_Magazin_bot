from aiogram.fsm.state import State, StatesGroup


class ProductState(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()