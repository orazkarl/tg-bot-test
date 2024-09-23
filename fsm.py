from aiogram.fsm.state import StatesGroup, State


class PatientFSM(StatesGroup):
    name = State()
    birthdate = State()
