from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.callback_data import CallbackData

from loader import dp
from aiogram.dispatcher import FSMContext
from states.holatlar import *
from api import *
from keyboards.default.main import *

@dp.message_handler(text='➕ Jamoa qo\'shish')
async def team(message: types.Message):
    telegram_id = message.from_user.id
    team = get_team(telegram_id=telegram_id)
    if team:
        await message.answer("🚫 Kechirasiz sizda allaqachon Jamoa yaratilgan !\n"
                             "Siz boshqa yangi Jamoa qo'sha olmaysiz !",reply_markup=team_keyboard)
    else:
        await message.answer('Jamoa nomini kiriting  : ')
        await TeamState.name.set()


@dp.message_handler(state=TeamState.name)
async def get_team_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({
        "name": name
    })
    data = await state.get_data()
    name = data['name']
    telegram_id = message.from_user.id
    create_team(name=name, captain=telegram_id)
    await message.answer("✅ Jamoa nomi qo'shildi",reply_markup=team_keyboard)
    await state.finish()


@dp.message_handler(text="➕ A'zo qo'shish")
async def add_member(message: types.Message):
    await message.answer("Jamoa a'zosini Ism Familiyasini kiriting : ")
    await MemberState.name.set()

@dp.message_handler(state=MemberState.name)
async def get_member_name(message:types.Message,state:FSMContext):
    name = message.text
    await state.update_data({
        'name': name
    })
    await message.answer("Telefon raqamini kiriting : ")
    await MemberState.phone_number.set()

@dp.message_handler(state=MemberState.phone_number)
async def get_member_phone(message:types.Message,state:FSMContext):
    phone_number = message.text
    await state.update_data({
        'phone_number':phone_number
    })
    await message.answer("Jamoa a'zosini raqamini kiriting : ")
    await MemberState.number.set()

@dp.message_handler(state=MemberState.number)
async def get_member_number(message:types.Message,state:FSMContext):
    number = message.text
    await state.update_data({
        'number':number
    })
    data = await state.get_data()
    name = data['name']
    phone_number = data['phone_number']
    number = data['number']
    telegram_id = message.from_user.id
    create_member(name=name,phone_number=phone_number,number=number,captain=telegram_id)
    await message.answer("Jamoa a'zosi qo'shildi ! ",reply_markup=team_keyboard)
    await state.finish()



action_cb = CallbackData("action", "value")
@dp.message_handler(text="👀 A'zolarni ko'rish")
async def show_member(message:types.Message):
    telegram_id = message.from_user.id
    member = get_member(telegram_id=telegram_id)
    if member:
        for i, j in enumerate(member):
            button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=" 📝 O'zgartirish", callback_data=action_cb.new(value=f"edit{member[i]['id']}")),
                        InlineKeyboardButton(text=" ❌ O'chirish",callback_data=action_cb.new(value=f"delete{member[i]['id']}"))
                    ]
                ]
            )
            await message.answer(f"🔢  ID : {i+1}\n"
                                 f"🙎‍♂  Ism familiyasi :  {member[i]['name']}\n"
                                 f"📞  Telefon raqami :  {member[i]['phone_number']}\n"
                                 f"#️⃣  O'yin raqami :  {member[i]['number']}\n",reply_markup=button)
    else:
        await message.answer("Jamoaga a'zolar qo'shilmagan",reply_markup=team_keyboard)

async def action_callback_handler(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data["value"]
    if value.startswith("delete"):
        await callback_query.answer(cache_time=60)
        member_id = value[6:]
        delete_member(member_id=member_id)
        await callback_query.message.answer("✅ O'chirildi",reply_markup=team_keyboard)
    else:
        await callback_query.answer(cache_time=60)
        await callback_query.message.answer("O'zgartirish kerak bo'lgan Ism Familiyasini kiriting : ")
        await MemberUpdateState.name.set()
        await state.update_data({
            'member_id': value[4:]
        })


@dp.message_handler(state=MemberUpdateState.name)
async def get_member_name(message: types.Message, state: FSMContext):
    member_name = message.text
    await state.update_data({
        'member_name': member_name
    })
    await message.answer("O'zgarishi kerak bo'lgan telefon raqamni kiriting : ")
    await MemberUpdateState.phone_number.set()


@dp.message_handler(state=MemberUpdateState.phone_number)
async def get_member_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data({
        'phone_number': phone_number
    })
    await message.answer("Jamoa a'zosini raqamini kiriting : ")
    await MemberUpdateState.number.set()

@dp.message_handler(state=MemberUpdateState.number)
async def get_member_number(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data({
        'number': number
    })
    data = await state.get_data()
    member_id = data['member_id']
    member_name = data['member_name']
    phone_number = data['phone_number']
    number = data['number']
    result = update_member(member_id=member_id, name=member_name, phone_number=phone_number, number=number)
    if result == 206:
        await message.answer("✅ Jamoa a'zosi o'zgartirildi ! ", reply_markup=team_keyboard)
        await state.finish()
    else:
        await message.answer('Kechirasiz xatolik yuz berdi!\n'
                             'Jarayonni boshidan boshlang ')
        await TeamUpdateState.name.set()

dp.register_callback_query_handler(action_callback_handler, action_cb.filter())


team_cb = CallbackData("team", "qiymat")
@dp.message_handler(text="👀 Jamoani ko'rish")
async def view(message:types.Message):
    telegram_id = message.from_user.id
    team = get_team(telegram_id)

    if team:
        team_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=" 📝 O'zgartirish",callback_data=team_cb.new(qiymat=f"team_edit{str(team[0]['id'])}")),
                    InlineKeyboardButton(text=" ❌ O'chirish", callback_data=team_cb.new(qiymat=f"team_delete{str(team[0]['id'])}"))

                ]
            ]
        )
        await message.answer(f"⚽️ Jamoani nomi : {team[0]['name']}\n"
                             f"🙎‍♂ Jamoa sardori : {team[0]['captain']['fullname']}",reply_markup=team_button)
    else:
        await message.answer("Kechirasiz sizda hali jamoa yaratilmagan ! ")

async def team_callback_handler(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data["qiymat"]
    if value.startswith("team_delete"):
        team_id = value[11:]
        delete_team(team_id)
        await callback_query.answer(cache_time=60)
        await callback_query.message.answer("✅ O'chirildi",reply_markup=team_keyboard)
    else:
        await callback_query.answer(cache_time=60)
        await callback_query.message.answer("Jamoa nomini kiriting : ")
        await TeamUpdateState.name.set()
        await state.update_data({
            'id':value[9:]
        })

@dp.message_handler(state=TeamUpdateState.name)
async def get_team_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({
        "name": name
    })
    data = await state.get_data()
    name = data['name']
    id = data['id']
    telegram_id = message.from_user.id

    result = update_team(id=id,telegram_id=telegram_id,name=name)
    if result == 206:
        await message.answer("✅ Jamoa nomi o'zgartirildi",reply_markup=team_keyboard)
        await state.finish()
    else:
        await message.answer("🚫 Kechirasiz bu nom allaqachon olingan !\n"
                             "Boshqa nom kiriting : ")
        await TeamUpdateState.name.set()
dp.register_callback_query_handler(team_callback_handler, team_cb.filter())


@dp.message_handler(text='📊 Statistic')
async def static(message:types.Message):
    telegram_id = message.from_user.id
    team = get_team(telegram_id=telegram_id)
    await message.answer(f"⚽️ Jamoa nomi : {team[0]['name']}\n"
                         f"🔢 O'tkizgan o'yinlar soni : {team[0]['matches_number']} ta.\n"
                         f"🏆 G'alabalar soni :  {team[0]['win_number']} ta.\n"
                         f"⁉️ Mag'lubiyatlar soni :  {team[0]['fail_number']} ta.\n"
                         f"🟰 Duranglar soni :  {team[0]['draw_number']} ta.\n")

@dp.message_handler(text='📚 Info')
async def info(message:types.Message):
    await message.answer("Bu bot futbol o'yinlarini uyushtirib beradigan bot.")

@dp.message_handler(text="⬅️ orqaga")
async def back(message:types.Message):
    await message.answer("Kerakli bo'limni tanlang : ",reply_markup=main_button)
