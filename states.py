from aiogram.dispatcher.filters.state import State, StatesGroup


class CurStates(StatesGroup):
    ADDSTATE = State()
    DELETESTATE = State()
    SHOWSTATE = State()
