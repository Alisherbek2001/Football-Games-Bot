from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.main import main_button, contact,team_keyboard
from states.holatlar import Register,TeamState
from api import *

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, Bo'timizdan foydalanish uchun /register buyrug'ini bosing")


@dp.message_handler(commands='menu')
async def menu(message:types.Message):
    await message.answer("Kerakli bo'limni tanlang : ",reply_markup=main_button)

@dp.message_handler(commands="register")
async def register(message: types.Message):
    await message.answer("Ism Familiyangizni kiriting:")
    await Register.fullname.set()

@dp.message_handler(state=Register.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data({
        "fullname": fullname
    })
    await message.answer("Raqamingizni yuboring:", reply_markup=contact)
    await Register.contact.set()


@dp.message_handler(state=Register.contact,content_types=types.ContentType.CONTACT,is_sender_contact=True)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact['phone_number']
    await state.update_data({
        "phone_number": phone_number
    })
    data = await state.get_data()
    fullname = data['fullname']
    telegram_id = message.from_user.id
    phone = data['phone_number']
    create_user(fullname=fullname,telegram_id=telegram_id,phone=phone)

    await message.answer(f"Kerakli bo'limni tanlang : ",reply_markup=main_button)
    await state.finish()


@dp.message_handler(text='🙎‍♂️ Team')
async def team(message: types.Message):
    await message.answer('Kerakli bo\'limni tanlang : ',reply_markup=team_keyboard)
