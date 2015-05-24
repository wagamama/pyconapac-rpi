from lib.rfid_mfrc522 import read_rfid
from lib import info
import requests
import logging

api = 'http://codeme.krdai.info/api/checkin/'

print info.MACHINE_ID, info.SD_ID

for index, uid in enumerate(read_rfid()):
    print index, uid

    try:
        r = requests.post(api, {
            'rfid': uid,
            'mid': info.MACHINE_ID,
        })
        assert r.status_code == requests.codes.ok, r.text
    except Exception as e:
        logging.exeption(e)

    # beep!!
