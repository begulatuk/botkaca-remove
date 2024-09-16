from pyrogram import Client, filters 
from pyrogram.types import Message
from bot import LOCAL, CONFIG, STATUS

@Client.on_message(filters.text & ~filters.chat(chats=STATUS.CHAT_ID))
async def func(client : Client, message: Message):
    if message.chat.type == "private":
        try:
            await message.delete()
        except:
            pass
    else:
        await message.reply_text(
            LOCAL.WRONG_ROOM.format(
                CHAT_ID = message.from_user.id            
            )
        )
