#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru, https://t.me/Sl_Sanda_Ru

from operator import gt
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from handlers.dbhandle import join_search, CONN
from handlers.messages import *
from handlers.gtrans import gtrans
from os import environ

# Chunker Function Copied From Stackoverflow https://stackoverflow.com/questions/434287/how-to-iterate-over-a-list-in-chunks/434328#434328
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

bot = Client(
    "En-To-Si-Bot",
    bot_token=environ['BOT_TOKEN'],
    api_hash=environ['API_HASH'],
    api_id=environ['API_ID']
    )
@bot.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=WELCOME_MESSAGE,reply_to_message_id=message.id,
    reply_markup=InlineKeyboardMarkup(WELCOME_KEY))
@bot.on_message(filters.private & filters.text)
async def trans(client, message):
    if len(message.text.strip().split()) > 1:
        await  message.reply_text('✅ ' + gtrans(message.text.strip() + '\nBot By :\t@Sandaru_Ashen'),reply_to_message_id = message.id)
    elif join_search(CONN,message.text.lower())[0] is True:
        await message.reply_text(text ='✅ ' + '\n✅ '.join(join_search(CONN,message.text)[1] + '\nBot By :\t@Sandaru_Ashen'),reply_to_message_id = message.id)
    elif join_search(CONN,message.text)[0] is False:
        keyboard = []
        for i in chunker(join_search(CONN,message.text)[1],2):
            try:
                keyboard.append(
                    [
                        InlineKeyboardButton(i[0],callback_data=i[0]),
                        InlineKeyboardButton(i[1],callback_data=i[1])
                    ])
            except IndexError:
                keyboard.append(
                    [
                        InlineKeyboardButton(i[0],callback_data=i[0])
                    ])
        keyboard = InlineKeyboardMarkup(keyboard)
        await  message.reply_text("No Results Found\nDo You Meant👇",reply_to_message_id = message.id, reply_markup = keyboard)
@bot.on_callback_query()
async def callback(client, update):
    if join_search(CONN,update.data)[1][0] != '':
        await update.message.edit('✅ ' + '\n✅ '.join(join_search(CONN,update.data)[1]) + '\nBot By :\t@Sandaru_Ashen')
    else:
        await update.message.edit('✅ ' + gtrans(update.data) + '\nBot By :\t@sandaru_ashen')
if __name__ == '__main__':
    print("Bot Started Running...")
    bot.run()
