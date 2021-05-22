from pyrogram import Client
from pyrogram.types import Message
from bot import LOCAL, CONFIG

async def func(client : Client, message: Message):
    chat_type = message.chat.type
    if message.chat.type != "private":
        await message.reply_text(
            LOCAL.WRONG_ROOM.format(
                CHAT_ID = message.chat.id
            )
        )    
