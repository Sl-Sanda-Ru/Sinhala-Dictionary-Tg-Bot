from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

WELCOME_MESSAGE = '''<b>Hello</b> There!👋🏻
Welcome To English To Sinhala Bot
Just Send Me An English Word Or Sentence & I Will Translate For You 🤖

<b>ආයුබෝවන්</b> 🙏
ඉංග්‍රීසි - සිංහල ශබ්දකෝෂයට සාදරයෙන් පිළිගන්නවා 📖
මට වචනයක් හෝ වාක්‍යයක් එවන්න මම එය පරිවර්තනය කර දෙන්නම් 🤖
'''
WELCOME_KEY = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Repo 🌎', url='https://github.com/Sl-Sanda-Ru/Sinhala-Dictionary-Tg-Bot'),
        InlineKeyboardButton('Contact Dev 🧑', url='https://t.me/Sl_Sanda_Ru')
    ]
])
SEL_LANG_MESSAGE = '''Select Bot Language
ඔබගේ භාෂාව තෝරන්න
        👇'''
SEL_LANG_KEY = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('Sinhala 🇱🇰', callback_data='sin'),
        InlineKeyboardButton('English 🇬🇧', callback_data='eng')
    ]
])
SET_LANG_ENG = '''✅ English Is Set As The Bot Language
If You Want To Change The Language Use /bot_language Command'''
SET_LANG_SIN = '''✅ සිංහල භාෂාව තෝරාගන්නා ලදි
ඔබට භාෂාව වෙනස් කිරීමට අවශ්‍ය නම් /bot_language විධානය භාවිත කරන්න'''

ALL_LANGS_MESSAGE_EN = '''This Feature Allows You To Translate Not Only English But Also Other Languages To Sinhala
You Have Currently {} This Feature'''
ALL_LANGS_MESSAGE_SIN = '''මෙම විශේෂාංගය මගින් ඉංග්‍රීසි භාෂාවට අමතරව වෙනත් භාෂාද සිංහලට පරිවර්තනය කිරීමට ඉඩ ලබා දේ
ඔබ මෙය {} කර ඇත'''

ALL_LANGS_KEYBOARD_DIS = InlineKeyboardMarkup([[InlineKeyboardButton('🚫 Disable',callback_data='dis')]])
ALL_LANGS_KEYBOARD_ENA = InlineKeyboardMarkup([[InlineKeyboardButton('✅ Enable',callback_data='ena')]])
ALL_LANGS_KEYBOARD_DIS_SIN = InlineKeyboardMarkup([[InlineKeyboardButton('🚫 අක්‍රීය කරන්න',callback_data='dis')]])
ALL_LANGS_KEYBOARD_ENA_SIN = InlineKeyboardMarkup([[InlineKeyboardButton('✅ සක්‍රීය කරන්න',callback_data='ena')]])

NO_RES_SUGG_EN = '''🚫 No Results Found
Do You Meant👇'''
NO_RES_SUGG_SIN = '''🚫 ප්‍රතිඵල කිසිවක් හමු නොවීය
ඔබ අදහස් කරේ👇'''
NO_RES_EN = '🚫 No Results!\nDetected Language: **{}**\nTo Translate Other Languages To Sinhala Use /all_languages Command'
NO_RES_SIN = '🚫 ප්‍රතිඵල කිසිවක් හමු නොවීය!\n**{}** භාෂාව හඳූනා ගන්නා ලදි, වෙනත් භාෂා පරිවර්තනය කිරීමට /all_languages විධානය භාවිත කරන්න'
NO_MED_EN = '🚫 Speech-to-Text and Optical Character Recognition are Not Suppored Yet.'
NO_MED_SIN = '🚫 කථන හඳුනාගැනීමේ සහ දෘශ්‍ය අක්ෂර හඳුනාගැනීමේ විශේෂාංග තවමත් එක්කර නැත'