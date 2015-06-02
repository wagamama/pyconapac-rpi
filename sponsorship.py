from lib.rfid_mfrc522 import read_rfid
from lib.buzzer import BuzzManager
from lib import info
import requests
import logging
import time

api = 'http://codeme.krdai.info/api/checkin/'

print info.MACHINE_ID, info.SD_ID

with BuzzManager(12) as buzzer:
    for index, uid in enumerate(read_rfid()):
        print index, uid

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
            buzzer.buzz(duration=0.5)
        except Exception as e:
            logging.exception(e)
