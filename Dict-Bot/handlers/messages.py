from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
WELCOME_MESSAGE = '''<b>Hello</b> There!👋🏻 Welcome To English To Sinhala Bot
Just Send Me An English Word Or Sentence & I Will Translate For You ☺️'''
WELCOME_KEY = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Repo 🌎', url='https://github.com/Sl-Sanda-Ru/Sinhala-Dictionary-Tg-Bot'),
        InlineKeyboardButton('Contact Dev 🧑', url='https://t.me/Sl_Sanda_Ru')
    ]
])
ALL_LANGS_MESSAGE = '''<b>Hello There!</b> This Feature Allows You To Translate Not Only English But Also Other Languages To Sinhala
You Have Currently {} This Feature'''
ALL_LANGS_KEYBOARD_DIS = InlineKeyboardMarkup([[InlineKeyboardButton('🚫 Disable',callback_data='dis')]])
ALL_LANGS_KEYBOARD_EN = InlineKeyboardMarkup([[InlineKeyboardButton('✅ Enable',callback_data='en')]])