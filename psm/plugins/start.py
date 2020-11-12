from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from psm import psm
from psm.plugins.helpers import dynamic_data_filter
from psm.plugins.texts import helptext, helptext1, helptext2, helptext3, tiptext1


@psm.on_message(filters.command("start"))
async def alive(_, message):
    buttons = [[InlineKeyboardButton("How it works", callback_data="help_1")]]
    await message.reply(helptext, reply_markup=InlineKeyboardMarkup(buttons))


@psm.on_callback_query(dynamic_data_filter("help_1"))
async def help_button(_, query):
    buttons = [[InlineKeyboardButton("Next", callback_data="help_2")]]
    await query.message.edit(
        helptext1,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    await query.answer()


@psm.on_callback_query(dynamic_data_filter("help_2"))
async def help_button1(_, query):
    buttons = [
        [
            InlineKeyboardButton("Previous", callback_data="help_1"),
            InlineKeyboardButton("Next", callback_data="help_3"),
        ]
    ]
    await query.message.edit(helptext2, reply_markup=InlineKeyboardMarkup(buttons))
    await query.answer()


@psm.on_callback_query(dynamic_data_filter("help_3"))
async def help_button2(_, query):
    buttons = [
        [
            InlineKeyboardButton("Previous", callback_data="help_2"),
            InlineKeyboardButton("Tip", callback_data="tip_1"),
        ]
    ]
    await query.message.edit(helptext3, reply_markup=InlineKeyboardMarkup(buttons))
    await query.answer()


@psm.on_callback_query(dynamic_data_filter("tip_1"))
async def tip_button1(_, query):
    buttons = [
        [
            InlineKeyboardButton("Previous", callback_data="help_3"),
            InlineKeyboardButton(
                "Source", url="https://github.com/pokurt/Pyrogram-SessionMaker-Bot"
            ),
        ]
    ]
    await query.message.edit(
        tiptext1,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )
    await query.answer()
