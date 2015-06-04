from lib.rfid_mfrc522 import read_rfid
from lib.buzzer import BuzzManager
from lib import info
import logging
import os

def check(uid):
    # check with server
    return True

with BuzzManager() as buzzer:
    for index, uid in enumerate(read_rfid()):
        print index, uid

        try:
            if check(uid):
                # user did register to this workshop
                # buzzer.buzz()
                os.system('sudo python /home/pi/pyconapac-rpi/lib/buzzer.py')

                # send to codeme server
            else:
                # user not register to this workshop
                os.system('sudo python /home/pi/pyconapac-rpi/lib/buzzer.py')
                os.system('sudo python /home/pi/pyconapac-rpi/lib/buzzer.py')
                os.system('sudo python /home/pi/pyconapac-rpi/lib/buzzer.py')

        except Exception as e:
            logging.exception(e)
