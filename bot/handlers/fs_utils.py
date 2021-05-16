import sys
import shutil
import os
import pathlib
import tarfile
from os.path import join as os_path_join
from bot import STATUS, CONFIG
from bot.plugins import aria2

workdir=os_path_join(CONFIG.ROOT, CONFIG.WORKDIR)

def start_cleanup():
    try:
        shutil.rmtree(workdir)
    except FileNotFoundError:
        pass

async def clean_all():
    STATUS.ARIA2_API = STATUS.ARIA2_API or aria2.aria2(
        config={
            'dir' : dir
        }
    )
    aria2_api = STATUS.ARIA2_API
    await aria2_api.start()
    aria2_api.remove_all(True)
    try:
        shutil.rmtree(workdir)
    except FileNotFoundError:
        pass

def exit_clean_up(signal, frame):
    try:
        LOGGER.info("Please wait, while we clean up the downloads and stop running downloads")
        clean_all()
        sys.exit(0)
    except KeyboardInterrupt:
        LOGGER.warning("Force Exiting before the cleanup finishes!")
        sys.exit(1)
