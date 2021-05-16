import pickle
from bot import LOCAL, CONFIG, STATUS, COMMAND
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from os import execl
from sys import executable


def sendMessage(text: str, client: Client, message: Message):
    try:
        return client.send_message(chat_id=message.chat.id,
                            reply_to_message_id=message.message_id,
                            text=text)
    except Exception as e:
        LOGGER.error(str(e))

@Client.on_message(filters.command(COMMAND.RESTART))
async def restart(client: Client, message: Message):
    restart_message = sendMessage(
        "Restarting, Please wait!",
        client,
        message
    )
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")
