# -*- coding: utf-8 -*-

import csv
import subprocess
import time
import sqlite3

DB_NAME = "pycon2015.db"
TABLE_NAME = "regist"

conn = sqlite3.connect(DB_NAME)
conn.isolation_level = None

f = open('pycon2015-regist.csv', 'r')

#sql = "BEGIN TRANSACTION;"

for row in csv.DictReader(f, ["reg_no", "ticket_type", "qrcode", "nickname", "email", "gender", "nationality", "food", "habbit", "tshirt", "company_name", "company_ubn", "fullname", "mobile", "zip", "address", "contact_name", "contact_email", "contact_mobile"]):

        str = "INSERT INTO regist (reg_no, ticket_type, qrcode, nickname, email, gender, nationality, food, habbit, tshirt, company_name, company_ubn, fullname, mobile, zip, address, contact_name, contact_email, contact_mobile) VALUES ('" + row['reg_no'] + "', '" + row['ticket_type'] + "', '" + row['qrcode'] + "', '" + row['nickname'] + "', '" + row['email'] + "', '" + row['gender'] + "', '" + row['nationality'] + "', '" + row['food'] + "', '" + row['habbit'] + "', '" + row['tshirt'] + "', '" + row['company_name'] + "', '" + row['company_ubn'] + "', '" + row['fullname'] + "', '" + row['mobile'] + "', '" + row['zip'] + "', '" + row['address'] + "', '" + row['contact_name'] + "', '" + row['contact_email'] + "', '" + row['contact_mobile'] + "');"

        conn.execute(str)

        print str

#sql += "COMMIT;"
#conn.executescript(sql)


