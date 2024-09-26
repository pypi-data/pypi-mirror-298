import logging
import os
from time import gmtime

def get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt="{levelname} {message}", style="{"))
    return console_handler

def init_logging():
    logging.Formatter.converter = gmtime
    root_log = logging.getLogger()
    root_log.addHandler(get_console_handler())
    root_log.setLevel(logging.WARNING)
    logging.getLogger('pandas').setLevel(logging.WARNING)
    logging.getLogger('geopandas').setLevel(logging.WARNING)
    logging.getLogger('rasterio').setLevel(logging.WARNING)
    logging.getLogger('PROJ').setLevel(logging.CRITICAL)
    
    os.environ['PROJ_DEBUG'] = '0'
