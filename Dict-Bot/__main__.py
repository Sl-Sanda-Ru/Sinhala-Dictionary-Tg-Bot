#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru, https://t.me/Sl_Sanda_Ru

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from handlers.messages import *
from handlers.search import join_search, result_format
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
    await message.reply_text(text=WELCOME_MESSAGE, reply_to_message_id=message.id, reply_markup=WELCOME_KEY)
    if search(message.from_user.id) is None:
        insert(message.from_user.id)
        await client.send_message(message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY)

@bot.on_message(filters.private & filters.command(['all_languages']))
async def alllangs(client, message):
    if search(message.from_user.id)[0] is False:
        await message.reply_text(
            text=ALL_LANGS_MESSAGE_SIN.format('🚫 අක්‍රීය') if search(message.from_user.id)[1] == 'sin' else ALL_LANGS_MESSAGE_EN.format('🚫 Disabled'),
            reply_to_message_id=message.id,
            reply_markup=ALL_LANGS_KEYBOARD_ENA_SIN if search(message.from_user.id)[1] == 'sin' else ALL_LANGS_KEYBOARD_ENA)
    else:
        await message.reply_text(
            text=ALL_LANGS_MESSAGE_SIN.format('✅ සක්‍රීය') if search(message.from_user.id)[1] == 'sin' else ALL_LANGS_MESSAGE_EN.format('🚫 Enabled'),
            reply_to_message_id=message.id,
            reply_markup=ALL_LANGS_KEYBOARD_DIS_SIN if search(message.from_user.id)[1] == 'sin' else ALL_LANGS_KEYBOARD_DIS)

@bot.on_message(filters.private & filters.command(['bot_language']))
async def botlang(client, message):
    await client.send_message(message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY)

@bot.on_message(filters.private & filters.text)
async def trans(client, message):
    if not search(message.from_user.id)[1]:
        await client.send_message(message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY)
        return
    if search(message.from_user.id)[0]:
        res = join_search(message.text.strip().lower(), any=True)
    else:
        res = join_search(message.text.strip().lower())
    if res[0] == 1:
        await message.reply_text(result_format(res[1]), reply_to_message_id = message.id)
    if res[0] == 2:
        if isinstance(res[1], list):
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
            await  message.reply_text(NO_RES_SUGG_SIN.format(res[1]) if search(message.from_user.id)[1] == 'sin' else NO_RES_SUGG_EN, reply_to_message_id = message.id, reply_markup = InlineKeyboardMarkup(keyboard))
        else:
            await message.reply_text(NO_RES_SIN.format(res[1]) if search(message.from_user.id)[1] == 'sin' else NO_RES_EN.format(res[1]), reply_to_message_id = message.id)

        # await client.pin_chat_message(chat_id=message.chat.id,message_id=message.id,both_sides=True)
@bot.on_callback_query()
async def callback(client, update):
    if update.data == 'dis':
        insert(update.from_user.id, status=False)
        await update.message.edit(
            text= ALL_LANGS_MESSAGE_SIN.format('🚫 අක්‍රීය') if search(update.from_user.id)[1] == 'sin' else ALL_LANGS_MESSAGE_EN.format('🚫 Disabled')
        )
            # reply_markup= ALL_LANGS_KEYBOARD_ENA_SIN if search(update.from_user.id)[1] == 'sin' else ALL_LANGS_KEYBOARD_ENA)
    elif update.data == 'ena':
        insert(update.from_user.id, status=True)
        await update.message.edit(
            text= ALL_LANGS_MESSAGE_SIN.format('✅ සක්‍රීය') if search(update.from_user.id)[1] == 'sin' else ALL_LANGS_MESSAGE_EN.format('✅ Enabled')
        )
            # reply_markup= ALL_LANGS_KEYBOARD_DIS_SIN if search(update.from_user.id)[1] == 'sin' else ALL_LANGS_KEYBOARD_DIS)
    elif update.data == 'eng':
        insert(update.from_user.id, lang=update.data)
        await update.message.edit(text=SET_LANG_ENG)
    elif update.data == 'sin':
        insert(update.from_user.id, lang=update.data)
        await update.message.edit(text=SET_LANG_SIN)
    else:
        await update.message.edit(result_format(join_search(update.data)[1]))

if __name__ == '__main__':
    print('Bot Started Running...')
    bot.run()
