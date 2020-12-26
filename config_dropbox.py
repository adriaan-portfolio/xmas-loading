from secrets import DBX_TOKEN
from os import environ
import logging
from dropbox import Dropbox

def create_dropbox_api():
    if "DBX_TOKEN" in globals():
        dbx = Dropbox(DBX_TOKEN)
    else:
        dbx = Dropbox(environ['DBX_TOKEN'])
    
    return dbx 
        