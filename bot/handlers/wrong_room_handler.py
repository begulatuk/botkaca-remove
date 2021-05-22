from pyrogram import Client
from pyrogram.types import Message
from bot import LOCAL, CONFIG

async def func(client : Client, message: Message):
    if message.chat.type != "private":
        await message.reply_text(
            LOCAL.WRONG_ROOM.format(
                CHAT_ID = message.from_user.id       
            )
        )
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    await message.delete(revoke=True)    

