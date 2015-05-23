#!/bin/bash

sqlite3 pycon2015.db "CREATE TABLE IF NOT EXISTS regist (reg_no TEXT PRIMARY KEY, uid TEXT, ticket_type TEXT, qrcode TEXT, nickname TEXT, email TEXT, gender TEXT, nationality TEXT, food TEXT, habbit TEXT, tshirt TEXT, company_name TEXT, company_ubn TEXT, fullname TEXT, mobile TEXT, zip TEXT, address TEXT, contact_name TEXT, contact_email TEXT, contact_mobile TEXT, attend_type TEXT, regist_wtime TEXT DEFAULT 0, tshirt_wtime TEXT DEFAULT 0, update_status INTEGER DEFAULT 0);"

