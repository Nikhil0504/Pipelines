import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def setup_file_handler(level):
    log_directory = "../logs"
    os.makedirs(log_directory, exist_ok=True)
    filename = datetime.now().strftime("cosmology_pipeline_%Y%m%d.log")
    filepath = os.path.join(log_directory, filename)
    
    file_handler = TimedRotatingFileHandler(filepath, when='midnight', interval=1, backupCount=7)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s'))
    
    return file_handler


def setup_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s'))
    
    return console_handler