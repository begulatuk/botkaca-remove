# GOAL:
# getting track for logging

import logging
import re
import urllib.parse
#import aiohttp
import requests

LOGGER = logging.getLogger(__name__)

# GOAL:
# create /leech handler
from bs4 import BeautifulSoup

from re import match as re_match
from asyncio import sleep as asyncio_sleep
from os.path import join as os_path_join
from math import floor
from pyrogram import Client, filters 
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aria2p.downloads import Download, File
from bot import LOCAL, STATUS, CONFIG, COMMAND
from bot.plugins import aria2, zipfile
from bot.handlers import upload_to_tg_handler
from bot.handlers import cancel_leech_handler
from bot.handlers.exceptions import DirectDownloadLinkException
from bot.handlers.direct_link_generator import direct_link_generator
from functools import partial

import asyncio
loop = asyncio.get_event_loop()
@Client.on_message(filters.command(COMMAND.LEECH))
async def func(client : Client, message: Message):
    args = message.text.split(" ")
    if len(args) <= 1:        
        try:
            await message.delete()
        except:
            pass
        return
    
    name_args = message.text.split("|")
    try:
        url = args[1]
    except IndexError:
        url = ''
    try:
        name = name_args[1].strip()
    except IndexError:
        name = ''
    LOGGER.info(args)
    LOGGER.info(url)
    LOGGER.info(name)
    reply = await message.reply_text(LOCAL.ARIA2_CHECKING_LINK)
    download_dir = os_path_join(CONFIG.ROOT, CONFIG.ARIA2_DIR)
    STATUS.ARIA2_API = STATUS.ARIA2_API or aria2.aria2(
        config={
            'dir' : download_dir
            
        }
    )
    aria2_api = STATUS.ARIA2_API
    await asyncio_sleep(int(CONFIG.EDIT_SLEEP))
    await aria2_api.start()
    text_url = url.strip()
    LOGGER.debug(f'Leeching : {text_url}')
    #LOGGER.info(f'Leeching : {text_url}')
    if "zippyshare.com" in text_url \
        or "osdn.net" in text_url \
        or "mediafire.com" in text_url \
        or "cloud.mail.ru" in text_url \
        or "cloud.mail.ru" in text_url \
        or "github.com" in text_url \
        or "yadi.sk" in text_url  \
        or "racaty.net" in text_url:
            try:
                urisitring = direct_link_generator(text_url)
                LOGGER.info(urisitring)
                link = [urisitring]
            except DirectDownloadLinkException as e:
                LOGGER.info(f'{text_url}: {e}')
        
    else:
        link = [text_url]
    try:
        #LOGGER.info(link)
        download = await loop.run_in_executor(None, partial(aria2_api.add_uris, link, options={
            'continue_downloads' : True,
            'bt_tracker' : STATUS.DEFAULT_TRACKER
            #'out': name
        }))       
    except Exception as e:
        if "No URI" in str(e):
            await reply.edit_text(
                LOCAL.ARIA2_NO_URI
            )
            return
        else:
            LOGGER.error(str(e))
            await reply.edit_text(
                str(e)
            )
            return

    if await progress_dl(reply, aria2_api, download.gid):
        download = await loop.run_in_executor(None, aria2_api.get_download, download.gid)
        if not download.followed_by_ids:
            download.remove(force=True)                   
            await upload_files(client, reply, abs_files(download_dir, download.files), os_path_join(download_dir, download.name + '.zip'))
        else:
            gids = download.followed_by_ids
            download.remove(force=True, files=True)
            for gid in gids:
                if await progress_dl(reply, aria2_api, gid):
                    download = await loop.run_in_executor(None, aria2_api.get_download, gid)
                    download.remove(force=True)
                    await upload_files(client, reply, abs_files(download_dir, download.files), os_path_join(download_dir, download.name + '.zip'))
        try:
            await reply.delete()
        except:
            pass

def abs_files(root, files):
    def join(file):
        return os_path_join(root, file.path)
    return map(join, files)

async def upload_files(client, reply, filepaths, zippath):
    if not STATUS.UPLOAD_AS_ZIP:
        for filepath in filepaths:
            await upload_to_tg_handler.func(
                filepath,
                client,
                reply,
                delete=True
            )
    else:
        zipfile.func(filepaths, zippath)
        await upload_to_tg_handler.func(
            zippath,
            client,
            reply,
            delete=True
        )

async def progress_dl(message : Message, aria2_api : aria2.aria2, gid : int, previous_text=None):
    try:
        download = await loop.run_in_executor(None, aria2_api.get_download, gid)
        if not download.is_complete:
            if not download.error_message:
                block = ""
                for i in range(1, int(CONFIG.BAR_SIZE) + 1):
                    if i <= floor(download.progress * int(CONFIG.BAR_SIZE)/100):
                        block += LOCAL.BLOCK_FILLED
                    else:
                        block += LOCAL.BLOCK_EMPTY
                text = LOCAL.ARIA2_DOWNLOAD_STATUS.format(
                    name = download.name,
                    block = block,
                    percentage = download.progress_string(),
                    total_size = download.total_length_string(),
                    download_speed = download.download_speed_string(),
                    upload_speed = download.upload_speed_string(),
                    seeder = download.num_seeders if download.is_torrent else 1,
                    eta = download.eta_string(),
                    gid = download.gid
                )
                if text != previous_text:
                    await message.edit(
                        text,
                        reply_markup=
                            InlineKeyboardMarkup([[
                                InlineKeyboardButton(
                                    COMMAND.CANCEL_LEECH,
                                    callback_data=COMMAND.CANCEL_LEECH + " " + download.gid,
                                    
                                )
                            ]])
                    )
                await asyncio_sleep(int(CONFIG.EDIT_SLEEP))
                return await progress_dl(message, aria2_api, gid, text)
            else:
                await message.edit(download.error_message)
        else:
            await asyncio_sleep(int(CONFIG.EDIT_SLEEP))
            await message.edit(
                LOCAL.ARIA2_DOWNLOAD_SUCCESS.format(
                    name=download.name
                )
            )
            return True
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await message.delete()
            return False
        elif " depth exceeded" in str(e):
            download.remove(force=True)
            await message.edit(
                LOCAL.ARIA2_DEAD_LINK.format(
                    name = download.name
                )
            )
            return False
        else:
            LOGGER.exception(str(e))
            await message.edit("<u>error</u> :\n<code>{}</code>".format(str(e)))
            return False
