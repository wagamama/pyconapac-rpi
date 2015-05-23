from rfid_mfrc522 import read_rfid

for index, uid in enumerate(read_rfid()):
    print index, uid
