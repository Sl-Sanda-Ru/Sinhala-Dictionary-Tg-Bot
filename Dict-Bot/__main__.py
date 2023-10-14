#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru, https://t.me/Sl_Sanda_Ru

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from handlers.messages import *
from handlers.search import definitions, result_format
from handlers.back import insert, search

# Chunker Function Copied From Stackoverflow https://stackoverflow.com/questions/434287/how-to-iterate-over-a-list-in-chunks/434328#434328
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

bot = Client(
    'Sinhala-Dictionary-Tg-Bot',
    bot_token = 'YOUR BOT TOKEN, OBTAIN IT FROM @BotFather',
    api_hash = 'YOUR API HASH, OBTAIN IT FROM https://my.telegram.org/auth',
    api_id = 1234
    )

@bot.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    if search(message.from_user.id) is None:
        insert(message.from_user.id)
    await message.reply_text(text=WELCOME_MESSAGE, reply_to_message_id=message.id, reply_markup=WELCOME_KEY)

@bot.on_message(filters.private & filters.command(['all_languages']))
async def alllangs(client, message):
    if search(message.from_user.id) is False:
        await message.reply_text(text=ALL_LANGS_MESSAGE.format('🚫 Disabled'), reply_to_message_id=message.id, reply_markup=ALL_LANGS_KEYBOARD_EN)
    else:
        await message.reply_text(text=ALL_LANGS_MESSAGE.format('✅ Enabled'), reply_to_message_id=message.id, reply_markup=ALL_LANGS_KEYBOARD_DIS)

@bot.on_message(filters.private & filters.text)
async def trans(client, message):
    if search(message.from_user.id):
        res = definitions(message.text, True)
    else:
        res = definitions(message.text)
    if res is None:
        await message.reply_text('🚫 No Results!', reply_to_message_id = message.id)
    elif res == 'no':
        await message.reply_text('🚫 No Results!\nTo Translate Other Languages To Sinhala Use /all_languages Command', reply_to_message_id = message.id)
    elif res[0] == 1:
        keyboard = []
        for i in chunker(res[1],2):
            try:
                keyboard.append(
                    [
                        InlineKeyboardButton(i[0], callback_data=i[0]),
                        InlineKeyboardButton(i[1], callback_data=i[1])
                    ])
            except IndexError:
                keyboard.append(
                    [
                        InlineKeyboardButton(i[0],callback_data=i[0])
                    ])
        await  message.reply_text('🚫 No Results Found\nDo You Meant👇', reply_to_message_id = message.id, reply_markup = InlineKeyboardMarkup(keyboard))
    else:
        # await client.pin_chat_message(chat_id=message.chat.id,message_id=message.id,both_sides=True)
        await message.reply_text(result_format(res), reply_to_message_id = message.id)

@bot.on_callback_query()
async def callback(client, update):
    if update.data == 'dis':
        insert(update.from_user.id)
        await update.message.edit(text=ALL_LANGS_MESSAGE.format('🚫 Disabled'), reply_markup=ALL_LANGS_KEYBOARD_EN)
    elif update.data == 'en':
        insert(update.from_user.id, status=True)
        await update.message.edit(text=ALL_LANGS_MESSAGE.format('✅ Enabled'), reply_markup=ALL_LANGS_KEYBOARD_DIS)
    else:
        await update.message.edit(result_format(definitions(update.data)))

if __name__ == '__main__':
    print('Bot Started Running...')
    bot.run()