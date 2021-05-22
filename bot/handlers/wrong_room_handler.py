from pyrogram import Client, filters 
from pyrogram.types import Message
from bot import LOCAL, CONFIG, STATUS

@Client.on_message(~filters.chat(chats=325093739))
async def func(client : Client, message: Message):
    if message.chat.type != "private":
        await message.reply_text(
            LOCAL.WRONG_ROOM.format(
                CHAT_ID = message.chat.id
            )
        )
    else:
        try:
            await message.delete()
        except:
            pass
