from datetime import datetime
import time

from database.smart_mode import SmartModeDB


def observer():
    while 1488:
        if datetime.now().minute <= 1:
            SmartModeDB.change_update_time()
        time.sleep(60 * 60)
if __name__ == "__main__":
    observer()