from os.path import join as os_path_join
from pyrogram import Client, filters 
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from bot import CONFIG, COMMAND, LOCAL, LOGGER, STATUS
from bot.handlers import *
from bot.handlers import fs_utils
import asyncio
import shutil
import signal
import pickle
from os import execl, path, remove

loop = asyncio.get_event_loop()

def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

        
    app = Client(
        "botkaca",
        bot_token=CONFIG.BOT_TOKEN,
        api_id=CONFIG.API_ID,
        api_hash=CONFIG.API_HASH,
        workers=100,
        workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR),
        plugins=dict(root="bot/handlers")
    )
    app.set_parse_mode("html")
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)
    app.run()
if __name__ == '__main__':
    main()
