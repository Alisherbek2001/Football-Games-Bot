from aiogram.dispatcher.filters.state import State,StatesGroup

class Register(StatesGroup):
    fullname = State()
    contact = State()

class TeamState(StatesGroup):
    name = State()

class TeamUpdateState(StatesGroup):
    name = State()


class MemberState(StatesGroup):
    name = State()
    phone_number = State()
    number = State()

class MemberUpdateState(StatesGroup):
    name = State()
    phone_number = State()
    number = State()