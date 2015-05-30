#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################
# Tabbed interface script
# www.sunjay-varma.com
###################################################

from Tkinter import *
import subprocess
import time
import sqlite3
import threading
import os
from web import Web
from db_controller import DBController
import json
import inspect
import json

DB_NAME = "pycon2015.db"
TABLE_NAME = "regist"
TAB1 = u"報到".encode('utf-8')
TAB2 = u"T恤".encode('utf-8')
TAB3 = u"新增".encode('utf-8')
TAB4 = "EXIT"
NOT_FOUND = "NOT FOUND"
VALUE_ERROR = "VALUE ERROR"
NFC_ERROR = "NFC ERROR"
NETWORK_ERROR = "NETWORK ERROR"
NO_UID_ERROR = "NO UID FOUND"

BASE = RAISED
SELECTED = FLAT

# a base tab class
class Tab(Frame, threading.Thread):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name

class TabBar(Frame, threading.Thread):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name
        threading.Thread.__init__(self)
        self.start()

    def show(self):
        self.pack(side=TOP, expand=YES, fill=X)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab

    def add(self, tab):
        tab.pack_forget()                                   # hide the tab on init

        self.tabs[tab.tab_name] = tab                       # add it to the list of tabs
        b = Button(self, text=tab.tab_name, relief=BASE,    # basic button stuff
            command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        b.pack(side=LEFT)                                               # pack the buttont to the left mose of self
        self.buttons[tab.tab_name] = b                                          # add it to the list of buttons

    def delete(self, tabname):

        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])

        else: del self.tabs[tabname]

        self.buttons[tabname].pack_forget()
        del self.buttons[tabname]

    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=BASE)
            self.tabs[self.current_tab].pack_forget()           # hide the current tab
        self.tabs[name].pack(side=BOTTOM)                           # add the new tab to the display
        self.current_tab = name                                 # set the current tab to itself

        self.buttons[name].config(relief=SELECTED)                  # set it to the selected style

        sv_reg_no.set("")
        sv_nickname.set("")
        sv_fullname.set("")
        sv_uid.set("")
        sv_pair_status.set("")
        sv_regist_status.set("")

        subprocess.call(['/home/pi/pyconapac-rpi/sh/kill_keyboard.sh'])

        if self.current_tab == TAB1 :
            print self.current_tab
            self.winfo_toplevel().wm_geometry("320x205+0+0")

        elif self.current_tab == TAB2 :
            print self.current_tab
            #self.winfo_toplevel().wm_geometry("320x110+0+95")
            self.winfo_toplevel().wm_geometry("320x205+0+0")

        elif self.current_tab == TAB3 :
            print self.current_tab
            self.winfo_toplevel().wm_geometry("320x110+0+95")
            subprocess.call(['/home/pi/pyconapac-rpi/sh/matchbox_keyboard_numpad.sh'])

        elif self.current_tab == TAB4 :
            print self.current_tab
            subprocess.call(['sudo', '/home/pi/pyconapac-rpi/sh/kill_touch.sh'])



    def run(self):
        w = Web()

        while True:
            print self.current_tab

            p = subprocess.Popen('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():

                if "error" in line:
                    print line
                    # error
                    sv_reg_no.set(NFC_ERROR)
                    sv_nickname.set(NFC_ERROR)
                    sv_uid.set(NFC_ERROR)

                if "UID (NFCID1)" in line:
                    global uid
                    uid_nfcid = line.split(":")
                    uid = uid_nfcid[1].strip(' \t\n\r')
                    os.system("sudo python /home/pi/pyconapac-rpi/buzzer.py &")

                    if self.current_tab == TAB1 :
                        tab1 = Tab1(root)
                        tab1.load_profile(uid)

                    elif self.current_tab == TAB2 :
                        tab2 = Tab2(root)
                        tab2.load_profile(uid)

                    elif self.current_tab == TAB3 :
                        sv_reg_no.set("");
                        sv_nickname.set("");
                        #tab3.load_profile(uid)

                        data = {'action':'query', 'uid':uid}
                        r = w.post(data);
                        j = json.loads(r.text)

                        print uid
                        sv_uid.set(uid)


            retval = p.wait()
            time.sleep(0.1)

class Tab1(Tab):
    def __init__(self, master):
        Tab.__init__(self, master, u"報到".encode('utf-8'))
        self.web = Web()
        self.db = DBController("/home/pi/pyconapac-rpi/db/pycon2015.db.nofacebook")
        self.reg_no = StringVar()
        self.nickname = StringVar()
        self.uid = StringVar()
        self.tshirt_wtime = StringVar()

        self.tab1_lbl_reg_no = Label(self, bg="red", fg="white", font=('Arial', 16), textvariable=sv_reg_no).pack(fill=X)
        self.tab1_lbl_nickname = Label(self, bg="green", fg="black", font=('Arial', 22), textvariable=sv_nickname).pack(fill=X)
        self.tab1_lbl_uid = Label(self, bg="blue", fg="white", font=('Arial', 20), textvariable=sv_uid).pack(fill=X)
        self.tab1_lbl_status = Label(self, bg="yellow", fg="black", font=('Arial', 22), textvariable=sv_regist_status).pack(side=LEFT, fill=BOTH, expand=YES)

    def load_profile(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        try:
            result = self.web.infoQuery(uid)
            status = result['result']['regist_wtime'] if result['result']['regist_wtime'] != '0' else 'First Check-in'
            reg_no = result['result']['reg_no']
            nickname = result['result']['nickname']
            user_info = self.db.getInfoByReg(reg_no)
            sv_reg_no.set(reg_no + "/" + user_info.ticket_type.split(' ')[-1])
            sv_nickname.set(nickname)
            sv_uid.set(uid)

            sv_regist_status.set(status)
            result = self.web.registerUpdate(reg_no, uid)

            # user_info = self.web.infoQuery(uid)
            # sv_reg_no.set(str(user_info['result']['reg_no']))
            # sv_nickname.set(str(user_info['result']['nickname']))
            # sv_uid.set(str(user_info['result']['uid']))
            # result = self.web.registerUpdate(user_info['result']['reg_no'], uid)
            print result

            # if user_info.regist_wtime == None:
            #     self.db.checkIn(uid)

        except ValueError:
            sv_reg_no.set(VALUE_ERROR)
            sv_nickname.set(VALUE_ERROR)
            sv_uid.set(uid)



class Tab2(Tab):
    def __init__(self, master):
        Tab.__init__(self, master, u"T恤".encode('utf-8'))
        self.web = Web()
        self.reg_no = StringVar()
        self.nickname = StringVar()
        self.tshirt = StringVar()
        self.tshirt_wtime = StringVar()
        self.pair_status = StringVar()

        self.tab2_fm1 = Frame(self)
        Label(self.tab2_fm1, bg="red", fg="white", width=16, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, fill=BOTH, expand=YES)
        Label(self.tab2_fm1, bg="green", fg="black", width=16, font=('Arial', 22), textvariable=sv_tshirt).pack(side=TOP, fill=BOTH, expand=YES)
        Label(self.tab2_fm1, bg="blue", fg="white", width=16, font=('Arial', 20), textvariable=sv_tshirt_wtime).pack(side=TOP, fill=BOTH, expand=YES)
        Label(self.tab2_fm1, bg="yellow", fg="black", width=16, font=('Arial', 22), textvariable=sv_tshirt_status).pack(side=LEFT, fill=BOTH, expand=YES)
        self.tab2_fm1.pack(side=LEFT, padx=10)

        self.tab2_fm2 = Frame(self)
        self.tab2_btn1 = Button(self.tab2_fm2, text='OK', font=('Arial', 16))
        self.tab2_btn1.pack(side=LEFT, anchor=W)
        self.tab2_btn1.bind('<Button-1>', self.get_tshirt)
        self.tab2_fm2.pack(side=LEFT, fill=BOTH, expand=YES)

    def get_tshirt(self, button):
        print type(self).__name__ + "/" + inspect.stack()[0][3]

        try:
            print uid
            result = self.web.tshirtUpdate(uid)
            sv_tshirt_wtime.set(result["result"]["tshirt_wtime"])
            sv_tshirt_status.set(result["status"])
            print result
            self.clear_profile()
        except NameError:
            sv_reg_no.set(NO_UID_ERROR)
            sv_tshirt.set(NO_UID_ERROR)
            sv_tshirt_wtime.set(NO_UID_ERROR)


    def load_profile(self, uid):
        print type(self).__name__ + "/" + inspect.stack()[0][3]

        user_info = self.web.tshirtQuery(uid)
        print user_info

        try:
            self.clear_get()

            sv_reg_no.set(str(user_info["result"]["reg_no"]) + "/" + user_info["result"]["nickname"])
            sv_tshirt.set(user_info["result"]["tshirt"])
            sv_tshirt_wtime.set(user_info["result"]["tshirt_wtime"])

            if user_info["result"]["tshirt_wtime"] != str(0):
                sv_tshirt_status.set("No T-shirt for you")

        except TypeError, ValueError:
            sv_reg_no.set(NETWORK_ERROR)
            sv_tshirt.set(NETWORK_ERROR)
            sv_tshirt_wtime.set(NETWORK_ERROR)

    def clear_profile(self):
        sv_reg_no.set("")
        sv_tshirt.set("")
        #sv_tshirt_wtime.set("")
        #sv_tshirt_status.set("")

    def clear_get(self):
        sv_tshirt_status.set("")


class Tab3(Tab):
    def __init__(self, master):
        Tab.__init__(self, master, u"新增".encode('utf-8'))

        self.web = Web()
        self.db = DBController("/home/pi/pyconapac-rpi/db/pycon2015.db")
        self.reg_no = StringVar()
        self.nickname = StringVar()
        self.fullname = StringVar()
        self.uid = StringVar()
        self.pair_status = StringVar()

        self.tab3_fm1 = Frame(self)
        self.txt3_fm1 = Text(self.tab3_fm1, width=3, height=1, font=('Arial', 12))
        self.txt3_fm1.pack(side=TOP, fill=X, expand=YES)
        self.txt3_fm1.focus()

        self.tab3_btn1 = Button(self.tab3_fm1, text='OK')
        self.tab3_btn1.pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.tab3_btn1.bind('<Button-1>', self.load_profile)
        self.tab3_fm1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tab3_fm2 = Frame(self)
        Label(self.tab3_fm2, bg="red", fg="white", width=12, font=('Arial', 16), textvariable=self.reg_no).pack(side=TOP, fill=BOTH, expand=YES)
        Label(self.tab3_fm2, bg="green", fg="black", width=12, font=('Arial', 10), textvariable=self.nickname).pack(side=TOP, fill=BOTH, expand=YES)
        Label(self.tab3_fm2, bg="blue", fg="white", width=12, font=('Arial', 16), textvariable=self.fullname).pack(side=TOP, fill=BOTH, expand=YES)
        self.tab3_fm2.pack(side=LEFT, padx=10)

        self.tab3_fm3 = Frame(self)
        self.tab3_lbl_uid = Label(self.tab3_fm3, bg="white", fg="black", width=10, font=('Arial', 12), textvariable=sv_uid).pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.tab3_btn1 = Button(self.tab3_fm3, text='Pair', font=('Arial', 10))
        self.tab3_btn1.pack(side=LEFT, anchor=W)
        self.tab3_btn1.bind('<Button-1>', self.pair_uid)
        self.tab3_lbl_pair_status = Label(self.tab3_fm3, bg="yellow", fg="black", width=4, font=('Arial', 24), textvariable=self.pair_status).pack(side=LEFT, fill=BOTH, expand=YES)
        self.tab3_fm3.pack(side=LEFT, fill=BOTH, expand=YES)

    def clear_profile(self):
        self.reg_no.set("")
        self.nickname.set("")
        self.fullname.set("")
        self.txt3_fm1.delete("1.0", "end")

    def clear_pair(self):
        sv_uid.set("")
        self.pair_status.set("")


    def load_profile(self, button):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        global reg_no
        reg_no = self.txt3_fm1.get("1.0", "end")
        user_info = self.db.getInfoByReg(int(reg_no))
        reg_no = user_info.reg_no
        self.reg_no.set(str(user_info.reg_no) + "/" + user_info.ticket_type.split(' ')[-1])
        self.nickname.set(user_info.nickname)
        self.fullname.set(user_info.fullname)
        self.clear_pair()

    def pair_uid(self, button):
        print type(self).__name__ + "/" + inspect.stack()[0][3]
        # from nfc import NFC
        # NFC('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll').read()
        try :
            result = self.web.registerUpdate(reg_no, uid)
            print result
            self.pair_status.set(result["status"])
        except NameError:
            print "NameError"
            self.pair_status.set("NameError")
        finally:
            self.clear_profile()



if __name__ == '__main__':
    def write(x): print x

    root = Tk()
    root.title("PyConAPAC 2015")
    root.geometry('320x205+0+0')

    global fullname
    global nickname
    global regist_wtime
    global tshirt_wtime
    global txt3_fm1

    sv_reg_no = StringVar()
    sv_name = StringVar()
    sv_nickname = StringVar()
    sv_fullname = StringVar()
    sv_uid = StringVar()
    sv_tshirt = StringVar()
    sv_tshirt_status = StringVar()
    sv_regist_status = StringVar()
    sv_regist_wtime = StringVar()
    sv_tshirt_wtime = StringVar()
    sv_pair_status = StringVar()
    sv_regist_count = StringVar()


    tabbar = TabBar(root, TAB1)

    tab1 = Tab1(root)
    tab2 = Tab2(root)
    tab3 = Tab3(root)
    tab4 = Tab(root, TAB4)

    tabbar.add(tab1)                   # add the tabs to the tab bar
    tabbar.add(tab2)                   # add the tabs to the tab bar
    tabbar.add(tab3)                   # add the tabs to the tab bar
    tabbar.add(tab4)

    #bar.config(bd=2, relief=RIDGE)         # add some border

    tabbar.show()

    root.mainloop()

