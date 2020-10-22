from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User, TermsOfService, ForceReply
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram import errors
import asyncio

from psm import psm, config

app = Client(":memory:", api_id=int(config.get('pyrogram', 'api_id')), api_hash=config.get('pyrogram', 'api_hash'))

code_caches = {}

@psm.on_message(filters.command('phone'))
async def phone_number(client, message):
    try:
        phonenum = message.text.split(None, 1)[1].replace(' ', '')
    except IndexError:
        await message.reply('Must pass args, example: `/phone +1234578900`')
        return
    try:
        await app.connect()
    except ConnectionError:
        await app.disconnect()
        await app.connect()
    try:
        sent_code = await app.send_code(phonenum)
    except FloodWait as e:
        await message.reply(f'I cannot create session for you.\nYou have a floodwait of: `{e.x} seconds`')
        return
    except errors.exceptions.bad_request_400.PhoneNumberInvalid:
        await message.reply('Phone number is invalid, Make sure you double check before sending.')
        return
    await message.reply('send me your code in 10 seconds, make sure you reply to this message', reply_markup=ForceReply(True))
    await asyncio.sleep(10)
    try:
        signed_in = await app.sign_in(phonenum, sent_code.phone_code_hash, code_caches[message.from_user.id])
    except KeyError:
        await message.reply('timed out, try again')
        return
    except errors.exceptions.bad_request_400.PhoneCodeInvalid:
        await message.reply('The code you sent seems Invalid, Try again.')
        return
    if isinstance(signed_in, User):
        return signed_in
    await app.send_message('me', f'```{(await app.export_session_string())}```')
    await app.stop()
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Go to Saved Messages', url=f'tg://user?id={message.from_user.id}')]]
    )
    await message.reply('All Done! Check your Saved Messages for your Session String.', reply_markup=button)

@psm.on_message(~filters.group, group=6)
async def code_save(client, message):
    try:
        if message.reply_to_message:
            code_caches[message.from_user.id] = message.text
        else:
            return
    except KeyError:
        await message.reply('Try using `/start` and read the instructions')
