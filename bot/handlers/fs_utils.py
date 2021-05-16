import sys
import shutil
import os
import pathlib
import magic
import tarfile

def start_cleanup():
    try:
        shutil.rmtree(DOWNLOAD_DIR)
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
