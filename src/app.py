import time
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from server import server
import database
from database.smart_mode import SmartModeDB

def observer():
    while 1488:
        if datetime.now().minute <= 1:
            SmartModeDB.change_update_time()
        time.sleep(60)

if __name__ == "__main__":
    p1 = Process(target=observer)
    p2 = Process(target=server)
    p1.start()
    p2.start()
