from lib.rfid_mfrc522 import read_rfid
from lib.buzzer import BuzzManager
from lib import info
import logging

def check(uid):
    # check with server
    return True

with BuzzManager() as buzzer:
    for index, uid in enumerate(read_rfid()):
        print index, uid

        try:
            if check(uid):
                # user did register to this workshop
                buzzer.buzz()
                # send to codeme server
            else:
                # user not register to this workshop
                buzzer.buzz(duration=0.5)

        except Exception as e:
            logging.exception(e)
