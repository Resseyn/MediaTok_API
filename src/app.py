import time
from datetime import datetime
from threading import Thread
from api import app
import database
from database.smart_mode import SmartModeDB

if __name__ == '__main__':
    app.run()
