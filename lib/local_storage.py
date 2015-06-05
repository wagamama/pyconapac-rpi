import sqlite3
import logging

def add(rfid, mid):
    try:
        with sqlite3.connect('rfid.db') as connect:
            connect.execute('''
                create table if not exists rfid(
                    rfid text,
                    mid text,
                    created timestamp DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            connect.execute('''
                insert into rfid(rfid, mid) values(?, ?)
            ''', (rfid, mid))

    except Exception as e:
        logging.exception(e)
