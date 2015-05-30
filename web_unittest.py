import unittest
import json
from web import Web

class TestDBAccess(unittest.TestCase):
    def setUp(self):
        self.web = Web()
        self.UID = '09  4d  06  02'

    def test_register(self):
        req = self.web.infoQuery(self.UID)
        self.assertEqual("60", req['result']['reg_no'])
        self.assertEqual("Bruce Tsai", req['result']['nickname'])
        req = self.web.registerUpdate(req['result']['reg_no'], self.UID)
        self.assertEqual("ok", req['status'])

    def test_query(self):
        req = self.web.infoQuery(self.UID)
        self.assertEqual("60", req['result']['reg_no'])
        self.assertEqual("Bruce Tsai", req['result']['nickname'])

    def test_tshirt_query(self):
        req = self.web.tshirtQuery(self.UID)
        self.assertEqual("M /160~170cm", req['result']['tshirt'])

    def test_tshirt_update(self):
        req = self.web.tshirtUpdate(self.UID)
        self.assertEqual("ok", req['status'])

if __name__ == '__main__':
    unittest.main()
