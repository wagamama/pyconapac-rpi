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
from nfc import NFC
from db_controller import DBController
from web import web

from db_controller import DBController

DB_NAME = "pycon2015.db"
TABLE_NAME = "regist"
TAB1 = u"報到".encode('utf-8')
TAB2 = u"T恤".encode('utf-8')
TAB3 = u"新增".encode('utf-8')
TAB4 = "EXIT"
NOT_FOUND = "NOT FOUND"

BASE = RAISED
SELECTED = FLAT

# a base tab class
class Tab(Frame, threading.Thread):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


class Tab3(Tab):
    def __init__(self, master):

        Tab.__init__(self, master, u"新增".encode('utf-8'))

        self.db = DBController("/home/pi/pyconapac-rpi/db/pycon2015.db")
        self.reg_no = StringVar()
        self.nickname = StringVar()
        self.attend_type = StringVar()

        self.tab3_fm1 = Frame(self)
        self.txt3_fm1 = Text(self.tab3_fm1, width=3, height=1, font=('Arial', 12))
        self.txt3_fm1.pack(side=TOP, fill=X, expand=YES)
        self.txt3_fm1.focus()

        self.tab3_btn1 = Button(self.tab3_fm1, text='OK')
        self.tab3_btn1.pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.tab3_btn1.bind('<Button-1>', self.load_profile)
        #self.tab3_btn1.bind('<Button-1>', tabbar.load_profile(3))
        self.tab3_fm1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tab3_fm2 = Frame(self)
        self.tab3_lbl_reg_no = Label(self.tab3_fm2, width=12, font=('Arial', 16), textvariable=self.reg_no).pack(side=TOP, fill=BOTH, expand=YES)
        self.tab3_lbl_nickname = Label(self.tab3_fm2, width=12, font=('Arial', 10), textvariable=self.nickname).pack(side=TOP, fill=BOTH, expand=YES)
        self.tab3_lbl_attend_type = Label(self.tab3_fm2, width=12, font=('Arial', 16), textvariable=self.attend_type).pack(side=TOP, fill=BOTH, expand=YES)
        self.tab3_fm2.pack(side=LEFT, padx=10)

        self.tab3_fm3 = Frame(self)
        self.tab3_lbl_uid = Label(self.tab3_fm3, width=6, font=('Arial', 12), textvariable=sv_uid).pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.tab3_btn1 = Button(self.tab3_fm3, text='Pair', font=('Arial', 10))
        #self.tab3_btn1.pack(side=TOP, anchor=W, expand=YES)
        self.tab3_btn1.pack(side=LEFT, anchor=W)
        self.tab3_btn1.bind('<Button-1>', self.pair_uid)
        self.tab3_lbl_pair_status = Label(self.tab3_fm3, width=1, font=('Arial', 10), textvariable=sv_pair_status).pack(side=LEFT, fill=BOTH, expand=YES)
        self.tab3_btn2 = Button(self.tab3_fm3, text='Unpair', font=('Arial', 10))
        self.tab3_btn2.pack(side=LEFT, anchor=E)
        self.tab3_btn2.bind('<Button-1>', self.unpair_uid)
        self.tab3_fm3.pack(side=LEFT, fill=BOTH, expand=YES)

    def load_profile(self, button):
        reg_no = self.txt3_fm1.get("1.0", "end")
        user_info = self.db.getInfoByReg(int(reg_no))
        self.reg_no.set(user_info.reg_no)
        self.nickname.set(user_info.nickname)
        self.attend_type.set(user_info.attend_type)

    def pair_uid(self, button):
        # from nfc import NFC
        # NFC('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll').read()
        print "pair"

    def unpair_uid(self, button):
        print "unpair"

# the bulk of the logic is in the actual tab bar

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

        if self.current_tab == TAB1 :
            self.winfo_toplevel().wm_geometry("320x205+0+0")
            subprocess.call(['/home/pi/pyconapac-rpi/sh/kill_keyboard.sh'])

        elif self.current_tab == TAB2 :
            self.winfo_toplevel().wm_geometry("320x205+0+0")
            subprocess.call(['/home/pi/pyconapac-rpi/sh/kill_keyboard.sh'])

        elif self.current_tab == TAB3 :
            self.winfo_toplevel().wm_geometry("320x110+0+95")
            subprocess.call(['/home/pi/pyconapac-rpi/sh/matchbox_keyboard_numpad.sh'])

        elif self.current_tab == TAB4 :
            subprocess.call(['/home/pi/pyconapac-rpi/sh/kill_keyboard.sh'])
            subprocess.call(['sudo', '/home/pi/pyconapac-rpi/sh/kill_touch.sh'])

    def run(self):

        while True:
            uid = NFC('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll').read()
            
            if self.current_tab == TAB1:
                dbc = DBController('/home/pi/pyconapac-rpi/db/pycon2015.db')
                user = dbc.getInfoByUid(uid)
                if user.data is None:
                    # Uid not found, show error message
                    sv_nickname.set('Uid not found')
                    sv_reg_no.set('')
                    sv_attend_type.set('')
                else:
                    dbc.setRegistTimeByUid(uid)
                    sv_nickname.set(user.nickname)
                    sv_reg_no.set(user.reg_no)
                    sv_attend_type.set(user.attend_type)

            elif self.current_tab == TAB2 :
                sv_uid.set(uid)
                cnnt = web()
                result = cnnt.tshirtQuery(uid)
                if result:
                    tsize, ttime = result
                    if ttime == 0:
                        sv_tshirt_size.set(tsize)
                        cnnt.tshirtUpdate()
                    else:
                        sb_nickname.set('No more T-shirt for you')
            else:
                pass


if __name__ == '__main__':
    def write(x): print x

    root = Tk()
    root.title("PyConAPAC 2015")
    root.geometry('320x205+0+0')

    global count_come
    global reg_no
    global fullname
    global nickname
    global attend_type
    global uid
    global regist_wtime
    global regist_status
    global tshirt_status
    global txt3_fm1
    global tshirt_size

    sv_reg_no = StringVar()
    sv_name   = StringVar()
    sv_nickname   = StringVar()
    sv_attend_type = StringVar()
    sv_uid = StringVar()
    sv_regist_status = StringVar()
    sv_tshirt_status = StringVar()
    sv_pair_status = StringVar()
    sv_regist_count = StringVar()
    sv_tshirt_size = StringVar()


    tabbar = TabBar(root, TAB1)

    tab1 = Tab(root, TAB1)
    tab1_lbl_reg_no = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_nickname = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_nickname).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_attend_type = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_attend_type).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_uid = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_uid).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_regist_status = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_regist_status).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_regist_count = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_regist_count).pack(side=TOP, expand=YES, fill=BOTH)


    tab2 = Tab(root, TAB2)
    tab1_lbl_reg_no = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_nickname = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_nickname).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_attend_type = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_attend_type).pack(side=TOP, expand=YES, fill=BOTH)
    tab1_lbl_tshirt_size = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_tshirt_size).pack(side=TOP, expand=YES, fill=BOTH)
    txt = Text(tab2, width=50, height=20)
    txt.pack(side=LEFT, fill=X, expand=YES)

    # tab3
    tab3 = Tab3(root)

    # tab4
    tab4 = Tab(root, TAB4)

    tabbar.add(tab1)                   # add the tabs to the tab bar
    tabbar.add(tab2)
    tabbar.add(tab3)
    tabbar.add(tab4)

    #bar.config(bd=2, relief=RIDGE)         # add some border

    tabbar.show()

    root.mainloop()

