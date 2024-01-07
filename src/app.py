import time
from datetime import datetime
from threading import Thread

from api import app
import database
from database.smart_mode import SmartModeDB


def observer():
    while 1488:
        SmartModeDB.change_update_time()
        time.sleep(60 * 60)

if __name__ == '__main__':
    obsTread = Thread(target=observer)
    appThread = Thread(target=app.run)
    obsTread.start()
    appThread.start()
