import unittest
import subprocess
import sqlite3
import os
from db_controller import DBController

DB_NAME = "pycon2015.db"

class TestDBAccess(unittest.TestCase):
    def setUp(self):
        subprocess.call(['../db/mkdb.sh'])
        conn = sqlite3.connect(DB_NAME)
        conn.isolation_level = None
        cursor = conn.cursor()
        cursor.execute("INSERT INTO regist (reg_no, fullname, nickname, uid, tshirt) VALUES ('01', 'John Dow', 'johndow', 'A1 B2', 'L')")
        cursor.execute("INSERT INTO regist (reg_no, fullname, nickname, uid, tshirt) VALUES ('02', 'Jane Dow', 'janedow', 'C3 D4', 'S')")
        conn.commit()
        self.db = DBController(DB_NAME)

    def tearDown(self):
        os.remove(DB_NAME)

    def test_checkIn(self):
        info = self.db.checkIn("A1 B2")
        self.assertIsNotNone(info.data)
        self.assertEqual("01", info.reg_no)
        self.assertEqual("A1 B2", info.uid)
        self.assertEqual("John Dow", info.fullname)
        self.assertEqual("johndow", info.nickname)
        self.assertIsNotNone(info.regist_wtime)

    def test_replace(self):
        info = self.db.getInfoByReg("02")
        self.assertIsNotNone(info.data)
        self.assertNotEqual("11 22", info.uid)
        info = self.db.pairUidByReg(info.reg_no, "11 22")
        self.assertEqual("11 22", info.uid)
        self.assertIsNotNone(info.regist_wtime)

    def test_tshirt(self):
        info = self.db.getInfoByUid("C3 D4")
        self.assertIsNotNone(info.data)
        self.assertIsNone(info.tshirt_wtime)
        info = self.db.setTshirtTimeByUid(info.uid)
        self.assertIsNotNone(info.tshirt_wtime)

    def test_needUpdate(self):
        self.db.checkIn("A1 B2")
        self.db.checkIn("C3 D4")
        infoList = self.db.getNeedUpdate()
        self.assertNotEqual(0, len(infoList))
        self.assertEqual("01", infoList[0].reg_no)
        self.assertEqual("A1 B2", infoList[0].uid)
        self.assertEqual("John Dow", infoList[0].fullname)
        self.assertEqual("johndow", infoList[0].nickname)
        self.assertFalse(infoList[0].update_status)
        self.assertEqual("02", infoList[1].reg_no)
        self.assertEqual("C3 D4", infoList[1].uid)
        self.assertEqual("Jane Dow", infoList[1].fullname)
        self.assertEqual("janedow", infoList[1].nickname)
        self.assertFalse(infoList[1].update_status)
        infoList = self.db.setUpdated(infoList)
        self.assertNotEqual(0, len(infoList))
        self.assertTrue(infoList[0].update_status)
        self.assertTrue(infoList[1].update_status)

    def test_getInfoByUids(self):
        uidList = ["A1 B2", "C3 D4"]
        infoList = self.db.getInfoByUids(uidList)
        self.assertNotEqual(0, len(infoList))
        self.assertEqual("A1 B2", infoList[0].uid)
        self.assertEqual("C3 D4", infoList[1].uid)

if __name__ == '__main__':
    unittest.main()
