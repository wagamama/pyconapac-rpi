from lib.rfid_mfrc522 import read_rfid
from lib.info import *

print info.MACHINE_ID, info.SD_ID

for index, uid in enumerate(read_rfid()):
    print index, uid
