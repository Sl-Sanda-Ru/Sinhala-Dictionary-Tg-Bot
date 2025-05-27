#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru, https://t.me/Sl_Sanda_Ru

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from handlers.messages import *
from handlers.search import join_search, result_format
from handlers.back import insert, search, get_all_id
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")
APP_ID = getenv("APP_ID")
BOT_TOKEN = getenv("BOT_TOKEN")
API_HASH = getenv("API_HASH")
ADMIN_ID = int(getenv("ADMIN_ID"))


# Chunker Function Copied From Stackoverflow https://stackoverflow.com/questions/434287/how-to-iterate-over-a-list-in-chunks/434328#434328
def chunker(seq, size):
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


bot = Client(
    "Sinhala-Dictionary-Tg-Bot", bot_token=BOT_TOKEN, api_hash=API_HASH, api_id=APP_ID
)


@bot.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
        text=WELCOME_MESSAGE, reply_to_message_id=message.id, reply_markup=WELCOME_KEY
    )
    if search(message.from_user.id) is None:
        insert(message.from_user.id)
        await client.send_message(
            message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY
        )


@bot.on_message(filters.private & ~filters.text)
async def media(client, message):
    await message.reply_text(
        text=NO_MED_SIN if search(message.from_user.id)[
            1] == "sin" else NO_MED_EN,
        reply_to_message_id=message.id,
    )


@bot.on_message(filters.private & filters.command(["all_languages"]))
async def alllangs(client, message):
    if search(message.from_user.id)[0] is False:
        await message.reply_text(
            text=(
                ALL_LANGS_MESSAGE_SIN.format("🚫 අක්‍රීය")
                if search(message.from_user.id)[1] == "sin"
                else ALL_LANGS_MESSAGE_EN.format("🚫 Disabled")
            ),
            reply_to_message_id=message.id,
            reply_markup=(
                ALL_LANGS_KEYBOARD_ENA_SIN
                if search(message.from_user.id)[1] == "sin"
                else ALL_LANGS_KEYBOARD_ENA
            ),
        )
    else:
        await message.reply_text(
            text=(
                ALL_LANGS_MESSAGE_SIN.format("✅ සක්‍රීය")
                if search(message.from_user.id)[1] == "sin"
                else ALL_LANGS_MESSAGE_EN.format("🚫 Enabled")
            ),
            reply_to_message_id=message.id,
            reply_markup=(
                ALL_LANGS_KEYBOARD_DIS_SIN
                if search(message.from_user.id)[1] == "sin"
                else ALL_LANGS_KEYBOARD_DIS
            ),
        )


@bot.on_message(filters.private & filters.command(["bot_language"]))
async def botlang(client, message):
    await client.send_message(
        message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY
    )


@bot.on_message(filters.private & filters.command(["forward"]))
async def forward(client, message):
    num = 0
    if message.from_user.id == ADMIN_ID:
        original = message.reply_to_message
        if not original:
            await message.reply(NOT_REPLIED)
            return
        if original.media_group_id:
            media_group = await client.get_media_group(original.chat.id, original.id)
            message_ids = [msg.id for msg in media_group]
            for id in get_all_id():
                try:
                    await client.forward_messages(
                        chat_id=id,
                        from_chat_id=original.chat.id,
                        message_ids=message_ids,
                    )
                except Exception:
                    continue
                else:
                    num += 1
        else:
            for id in get_all_id():
                try:
                    await original.forward(id)
                except Exception:
                    continue
                else:
                    num += 1
        await message.reply_text(BROAD_SENT.format(num), reply_to_message_id=message.id)
    else:
        await message.reply_text(NO_BROAD, reply_to_message_id=message.id)


@bot.on_message(filters.private & filters.text)
async def trans(client, message):
    if not search(message.from_user.id)[1]:
        await client.send_message(
            message.from_user.id, SEL_LANG_MESSAGE, reply_markup=SEL_LANG_KEY
        )
        return
    if search(message.from_user.id)[0]:
        res = join_search(message.text.strip().lower(), any=True)
    else:
        res = join_search(message.text.strip().lower())
    if res[0] == 1:
        await message.reply_text(result_format(res[1]), reply_to_message_id=message.id)
    if res[0] == 2:
        if isinstance(res[1], list):
            keyboard = []
            for i in chunker(res[1], 2):
                try:
                    keyboard.append(
                        [
                            InlineKeyboardButton(i[0], callback_data=i[0]),
                            InlineKeyboardButton(i[1], callback_data=i[1]),
                        ]
                    )
                except IndexError:
                    keyboard.append(
                        [InlineKeyboardButton(i[0], callback_data=i[0])])
            await message.reply_text(
                (
                    NO_RES_SUGG_SIN.format(res[1])
                    if search(message.from_user.id)[1] == "sin"
                    else NO_RES_SUGG_EN
                ),
                reply_to_message_id=message.id,
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await message.reply_text(
                (
                    NO_RES_SIN.format(res[1])
                    if search(message.from_user.id)[1] == "sin"
                    else NO_RES_EN.format(res[1])
                ),
                reply_to_message_id=message.id,
            )


@bot.on_callback_query()
async def callback(client, update):
    if update.data == "dis":
        insert(update.from_user.id, status=False)
        await update.message.edit(
            text=(
                ALL_LANGS_MESSAGE_SIN.format("🚫 අක්‍රීය")
                if search(update.from_user.id)[1] == "sin"
                else ALL_LANGS_MESSAGE_EN.format("🚫 Disabled")
            )
        )
    elif update.data == "ena":
        insert(update.from_user.id, status=True)
        await update.message.edit(
            text=(
                ALL_LANGS_MESSAGE_SIN.format("✅ සක්‍රීය")
                if search(update.from_user.id)[1] == "sin"
                else ALL_LANGS_MESSAGE_EN.format("✅ Enabled")
            )
        )
    elif update.data == "eng":
        insert(update.from_user.id, lang=update.data)
        await update.message.edit(text=SET_LANG_ENG)
    elif update.data == "sin":
        insert(update.from_user.id, lang=update.data)
        await update.message.edit(text=SET_LANG_SIN)
    else:
        await update.message.edit(result_format(join_search(update.data)[1]))


if __name__ == "__main__":
    print("Bot Started Running...")
    bot.run()
