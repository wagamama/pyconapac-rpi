# http://zetcode.com/db/sqlitepythontutorial/
import sqlite3
import inspect
from datetime import datetime

class db():
    name  = "db/pycon2015.db"
    table = "regist"
    conn  = None
    err   = {"reg_no" : None, "nickname" : "NOT FOUND!!"}

    def __init__(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.name)

    def fetch_one(self, reg_no):
        print inspect.stack()[0][3]
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT reg_no, uid, fullname, nickname, tshirt, attend_type, regist_wtime, tshirt_wtime FROM regist WHERE reg_no=?''', (reg_no,))
            #cursor.execute('''SELECT reg_no, uid, fullname, nickname, tshirt, attend_type, regist_wtime, tshirt_wtime FROM regist WHERE uid=?''', (uid,))
            rows = cursor.fetchall()
            for row in rows:
                #print row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                return {'reg_no' : row[0],
                        'uid' : row[1],
                        'fullname' : row[2],
                        'nickname' : row[3],
                        'tshirt' : row[4],
                        'attend_type' : row[5],
                        'regist_wtime' : row[6],
                        'tshirt_wtime' : row[7]}

            return self.err


    def fetch_all(self, kyword):
        print inspect.stack()[0][3]
        with self.conn:
            qstr = "SELECT reg_no, uid, fullname, nickname, tshirt, attend_type, regist_wtime, tshirt_wtime FROM regist WHERE "
            for k, v in kyword.items():
                qstr += str(k) + "='" + str(v) + "' AND "

            cursor = self.conn.cursor()
            cursor.execute(qstr[:-4])
            return cursor.fetchall()


    def update_one(self, reg_no, uid):
        print inspect.stack()[0][3]
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE regist SET uid=?, regist_wtime=? WHERE reg_no=?", (uid, str(datetime.now()), reg_no))        
            self.conn.commit()

            
    def insert_one(self, uid):
        pass

