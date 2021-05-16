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
def main(client: Client, message: Message):
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        message.edit_text(restart_message)
        remove('restart.pickle')
    
# Initialize bot
    app = Client(
        ":memory:",
        bot_token=CONFIG.BOT_TOKEN,
        api_id=CONFIG.API_ID,
        api_hash=CONFIG.API_HASH,
        workers=32,
        workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR),
        plugins=dict(root="bot/handlers")
    )
    app.UPDATES_WORKERS = 100
    app.DOWNLOAD_WORKERS = 100
    app.set_parse_mode("html")
    LOGGER.info("Bot Started!")
    # register /start handler
    app.add_handler(
        MessageHandler(
            start_message_handler.func,
            filters=filters.command(COMMAND.START)
        )
    )

    if CONFIG.BOT_PASSWORD:
        # register /pass handler
        app.add_handler(
            MessageHandler(
                password_handler.func,
                filters = filters.command(COMMAND.PASSWORD)
            )
        )

        # take action on unauthorized chat room
        app.add_handler(
            MessageHandler(
                wrong_room_handler.func,
                filters = lambda msg: not msg.chat.id in STATUS.CHAT_ID
            )
        )
    loop.create_task(app.run())
if __name__ == '__main__':
    main()
    #loop = asyncio.get_event_loop()
    #loop.create_task()
    #try:
    #    loop.run_forever()
    #except (KeyboardInterrupt, SystemExit):
    #    loop.run_until_complete(app.stop())
    #    loop.close()
