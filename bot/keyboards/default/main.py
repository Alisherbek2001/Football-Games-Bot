from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main_button = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🙎‍♂️ Team"),
        ],
        [
            KeyboardButton(text="📌 Match"),
            KeyboardButton(text="📋 Result")
        ],
        [
            KeyboardButton(text="🎞 Video"),
            KeyboardButton(text="📊 Statistic")
        ],
        [
            KeyboardButton(text="📚 Info")
        ]

    ]
)



contact = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📞 Share Contact",request_contact=True)
        ],
    ]
)



team_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='➕ Jamoa qo\'shish'),
            KeyboardButton(text='👀 Jamoani ko\'rish')
        ],
        [
            KeyboardButton(text="➕ A'zo qo'shish"),
            KeyboardButton(text="👀 A\'zolarni ko\'rish")
        ],
        [
            KeyboardButton(text='⬅️ orqaga')
        ]
    ]
)


