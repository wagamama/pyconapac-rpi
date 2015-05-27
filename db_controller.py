import sqlite3
import inspect
from datetime import datetime

INFO_FIELD = "reg_no, uid, fullname, nickname, tshirt, attend_type, regist_wtime, tshirt_wtime, scan_status, ticket_type"
NOT_FOUND = "NOT FOUND"

class Info:
    reg_no = NOT_FOUND
    uid = NOT_FOUND
    fullname = NOT_FOUND
    nickname = NOT_FOUND
    attend_type = NOT_FOUND
    regist_wtime = NOT_FOUND
    tshirt_wtime = NOT_FOUND
    ticket_type = NOT_FOUND

    def __init__(self, data=None):
        self.data = data
        if data is not None:
            self.reg_no = data[0]
            self.uid = data[1]
            self.fullname = data[2]
            self.nickname = data[3]
            self.tshirt = data[4]
            self.attend_type = data[5]
            self.regist_wtime = data[6] if data[6] != '0' else None
            self.tshirt_wtime = data[7] if data[7] != '0' else None
            self.scan_status = False if data[8] == 0 else True
            self.ticket_type = data[9]

    def __repr__(self):
        return str(self.data)

class DBController:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.isolation_level = None

    def __del__(self):
        self.conn.close()

    def setRegistTimeByUid(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE regist SET regist_wtime=? WHERE uid=?", (now, uid,))
        self.conn.commit()
        return self.getInfoByUid(uid)

    def setTshirtTimeByUid(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE regist SET tshirt_wtime=? WHERE uid=?", (now, uid,))
        self.conn.commit()
        return self.getInfoByUid(uid)

    def getInfoByReg(self, reg_no):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE reg_no=?"
        cursor.execute(sql, (reg_no,))
        all_rows = cursor.fetchall()
        if len(all_rows)!=1:
            return Info()
        else:
            return Info(all_rows[0])

    def getInfoByUid(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE uid=?"
        cursor.execute(sql, (uid,))
        all_rows = cursor.fetchall()
        if len(all_rows) == 1:
            return Info(all_rows[0])
        else:
            return Info()

    def getInfoByUids(self, uidList):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        if len(uidList)==0:
            return []

        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE uid IN "
        uids = []
        for uid in uidList:
            uids.append("'" + uid + "'")
        values = "(" + ",".join(uids) + ")"
        sql += values
        cursor = self.conn.cursor()
        cursor.execute(sql)
        all_rows = cursor.fetchall()
        infoList = []
        for row in all_rows:
            infoList.append(Info(row))
        return infoList

    def checkIn(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        info = self.getInfoByUid(uid)
        if info.data is not None:
            return self.setRegistTimeByUid(uid)
        return info

    def pairUidByReg(self, reg_no, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        cursor.execute("UPDATE regist SET uid=? WHERE reg_no=?", (uid, reg_no))
        self.conn.commit()
        return self.setRegistTimeByUid(uid)

    def getNeedUpdate(self):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE regist_wtime!='0' AND scan_status=0"
        cursor.execute(sql)
        all_rows = cursor.fetchall()
        infoList = []
        for row in all_rows:
            infoList.append(Info(row))
        return infoList

    def setUpdated(self, infoList):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        if len(infoList)==0:
            return []

        sql = "BEGIN TRANSACTION;"
        for info in infoList:
            sql += "UPDATE regist SET scan_status=1 WHERE reg_no='" + info.reg_no + "';"
        sql += "COMMIT;"
        self.conn.executescript(sql)
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE reg_no IN "
        regs = []
        for info in infoList:
            regs.append("'" + info.reg_no + "'")
        values = "(" + ",".join(regs) + ")"
        sql += values
        cursor = self.conn.cursor()
        cursor.execute(sql)
        all_rows = cursor.fetchall()
        infoList = []
        for row in all_rows:
            infoList.append(Info(row))
        return infoList
