from psm import psm

import asyncio
from pyrogram import filters
from psm.plugins.dictionaries import code_caches, app_ids, app_hashs, passwords


@psm.on_message(~filters.group, group=6)
async def code_save(client, message):
    try:
        if message.reply_to_message:
            code_caches[message.from_user.id] = message.text
        else:
            return
    except KeyError:
        await message.reply("Try using `/start` and read the instructions")


@psm.on_message(filters.command("appid"))
async def checkid(client, message):
    try:
        appid = message.text.split(None, 1)[1]
    except IndexError:
        await message.reply("Must pass args, example: `/appid 12345`")
        return
    app_ids[message.from_user.id] = appid
    await message.reply("Your `APP_ID` variable is set")


@psm.on_message(filters.command("apphash"))
async def checkhash(client, message):
    try:
        apphash = message.text.split(None, 1)[1]
    except IndexError:
        await message.reply("Must pass args, example: `/apphash abCd1234Fghe`")
        return
    app_hashs[message.from_user.id] = apphash
    await message.reply("Your `APP_HASH` variable is set")


@psm.on_message(filters.command("password"))
async def checkpass(client, message):
    try:
        password = message.text.split(None, 1)[1]
    except IndexError:
        await message.reply("Must pass args, example: `/password helloworld`")
        return
    passwords[message.from_user.id] = password
    await message.reply("Your `CLOUD_PASS` variable is set")


@psm.on_message(filters.command("clear"))
async def clear_dict(_, message):
    code_caches.pop(message.from_user.id, None)
    m = await message.reply("checking and clearing saved verification codes.")
    await asyncio.sleep(3)
    passwords.pop(message.from_user.id, None)
    await m.edit("checking and clearing saved cloud passwords.")
    await asyncio.sleep(3)
    app_ids.pop(message.from_user.id, None)
    await m.edit("checking and clearing saved api_id.")
    await asyncio.sleep(3)
    app_hashs.pop(message.from_user.id, None)
    await m.edit("checking and clearing saved api_hash.")
    await asyncio.sleep(3)
    await m.edit("all cleared")
    await asyncio.sleep(3)
    await message.delete()
    await m.delete()
