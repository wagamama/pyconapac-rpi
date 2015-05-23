import sqlite3

INFO_FIELD = "reg_no, uid, fullname, nickname, tshirt, attend_type, regist_wtime, tshirt_wtime, update_status"

class Info:
    reg_no = None
    uid = None
    fullname = None
    nickname = None
    attend_type = None
    regist_wtime = None

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
            self.update_status = False if data[8] == 0 else True

    def __repr__(self):
        return str(self.data)

class DBController:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.isolation_level = None

    def __del__(self):
        self.conn.close()

    def setRegistTimeByUid(self, uid):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE regist SET regist_wtime=DateTime('now', 'utc') WHERE uid=?", (uid,))
        self.conn.commit()
        return self.getInfoByUid(uid)

    def setTshirtTimeByUid(self, uid):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE regist SET tshirt_wtime=DateTime('now', 'utc') WHERE uid=?", (uid,))
        self.conn.commit()
        return self.getInfoByUid(uid)

    def getInfoByReg(self, reg_no):
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE reg_no=?"
        cursor.execute(sql, (reg_no,))
        all_rows = cursor.fetchall()
        if len(all_rows)!=1:
            return Info()
        else:
            return Info(all_rows[0])

    def getInfoByUid(self, uid):
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE uid=?"
        cursor.execute(sql, (uid,))
        all_rows = cursor.fetchall()
        if len(all_rows)!=1:
            return Info()
        else:
            return Info(all_rows[0])

    def getInfoByUids(self, uidList):
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
        info = self.getInfoByUid(uid)
        if info.data is not None:
            return self.setRegistTimeByUid(uid)
        return info

    def pairUidByReg(self, reg_no, uid):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE regist SET uid=? WHERE reg_no=?", (uid, reg_no))
        self.conn.commit()
        return self.setRegistTimeByUid(uid)

    def getNeedUpdate(self):
        cursor = self.conn.cursor()
        sql = "SELECT " + INFO_FIELD + " FROM regist WHERE regist_wtime!='0' AND update_status=0"
        cursor.execute(sql)
        all_rows = cursor.fetchall()
        infoList = []
        for row in all_rows:
            infoList.append(Info(row))
        return infoList

    def setUpdated(self, infoList):
        if len(infoList)==0:
            return []

        sql = "BEGIN TRANSACTION;"
        for info in infoList:
            sql += "UPDATE regist SET update_status=1 WHERE reg_no='" + info.reg_no + "';"
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
