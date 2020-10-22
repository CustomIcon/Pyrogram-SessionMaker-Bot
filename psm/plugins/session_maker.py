from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User, TermsOfService, ForceReply
from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio

from psm import psm, config
from psm.plugins.helpers import dynamic_data_filter
from psm.plugins.texts import helptext, helptext1, helptext2, tiptext1

app = Client(":memory:", api_id=int(config.get('pyrogram', 'api_id')), api_hash=config.get('pyrogram', 'api_hash'))

code_caches = dict()


@psm.on_message(filters.command('phone'))
async def phone_number(client, message):
    await message.reply('Telegram will send you an activation code, Send it to me to get your session string', reply_markup=ForceReply(True))
    try:
        phonenum = message.command[1]
    except IndexError:
        await message.reply('Must pass args, example: `/phone +1234578900')
        return
    await app.connect()
    try:
        sent_code = await app.send_code(phonenum)
    except FloodWait as e:
        await message.reply(f'I cannot create session for you.\nYou have a floodwait of: `{e.x}seconds``')
        return
    await message.reply('send me your code in 20 seconds, make sure you reply to this message')
    await asyncio.sleep(20)
    signed_in = await app.sign_in(phonenum, sent_code.phone_code_hash, code_caches[message.from_user.id])
    if isinstance(signed_in, User):
        return signed_in
    await message.reply(app.export_session_string())
    await app.stop()

@psm.on_message(filters.private)
async def code_save(client, message):
    if message.reply_to_message:
        code_caches[message.from_user.id] = message.text
        print(code_caches)
    else:
        return
