from os import execl
from sys import executable


@Client.on_message(filters.command(COMMAND.RESTART))
async def func(client: Client, message: Message):
     
    restart_message = await message.reply_text("Restarting, Please wait!")
    
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")
