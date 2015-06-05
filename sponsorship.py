from lib.rfid_mfrc522 import read_rfid
from lib import info
from lib import local_storage
import requests
import logging
import time
import os

api = 'http://codeme.krdai.info/api/checkin/'

print info.MACHINE_ID, info.SD_ID

for index, uid in enumerate(read_rfid()):
    print index, uid

    local_storage.add(uid, info.MACHINE_ID)

    try:
        r = requests.post(api, {
            'rfid': uid,
            'mid': info.MACHINE_ID,
            'data': "{}"
        })
        assert r.ok, r.text
    except Exception as e:
        logging.exeption(e)

    try:
        os.system('sudo python /home/pi/pyconapac-rpi/lib/buzzer.py')
    except Exception as e:
        logging.exception(e)
