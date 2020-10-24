from psm import psm
from pyrogram import filters
from psm.plugins.dictionaries import app_ids, app_hashs, passwords, code_caches


@psm.on_message(filters.command('variables'))
async def check_vars(client, message):
    try:
        text = f'**APP_ID**: `{app_ids[message.from_user.id]}`\n'
    except KeyError:
        text = '**APP_ID**: `None`\n'
    try:
        text += f'**APP_HASH**: `{app_hashs[message.from_user.id]}`\n'
    except KeyError:
        text += '**APP_HASH**: `None`\n'
    try:
        text += f'**PASSWORD**:`{passwords[message.from_user.id]}`\n'
    except KeyError:
        text += '**PASSWORD**: `None`\n'
    try:
        text += f'**VALIDATE_CODE**:`{code_caches[message.from_user.id]}`'
    except KeyError:
        text += '**VALIDATE_CODE**: `None`'
    await message.reply(text)