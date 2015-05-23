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
class Tab(Frame):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


# the bulk of the logic is in the actual tab bar

class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name

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
            print self.current_tab

            p = subprocess.Popen('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                if "UID (NFCID1)" in line:
                    uid_nfcid = line.split(":")
                    uid = uid_nfcid[1].strip(' \t\n\r')
                    print uid

            if self.current_tab == TAB1 :
                pass
            elif self.current_tab == TAB2 :
                pass
            else :
                pass

            retval = p.wait()
            time.sleep(1)



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

    sv_reg_no = StringVar()
    sv_name   = StringVar()
    sv_nickname   = StringVar()
    sv_attend_type = StringVar()
    sv_uid = StringVar()
    sv_regist_status = StringVar()
    sv_tshirt_status = StringVar()
    sv_pair_status = StringVar()
    sv_regist_count = StringVar()


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
    #tab1_lbl_tshirt_size = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_tshirt_size).pack(side=TOP, expand=YES, fill=BOTH)
    txt = Text(tab2, width=50, height=20)
    txt.pack(side=LEFT, fill=X, expand=YES)



    tab3 = Tab(root, TAB3)
    tab3_fm1 = Frame(tab3)
    txt3_fm1 = Text(tab3_fm1, width=3, height=1, font=('Arial', 12))
    txt3_fm1.pack(side=TOP, fill=X, expand=YES)
    txt3_fm1.focus()
    tab3_btn1 = Button(tab3_fm1, text='OK')
    tab3_btn1.pack(side=TOP, anchor=W, fill=X, expand=YES)
    #tab3_btn1.bind('<Button-1>', tabbar.load_profile)
    #tab3_btn1.bind('<Button-1>', tabbar.load_profile(3))
    tab3_fm1.pack(side=LEFT, fill=BOTH, expand=YES)

    tab3_fm2 = Frame(tab3)
    tab3_lbl_reg_no = Label(tab3_fm2, width=12, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, fill=BOTH, expand=YES)
    tab3_lbl_nickname = Label(tab3_fm2, width=12, font=('Arial', 10), textvariable=sv_nickname).pack(side=TOP, fill=BOTH, expand=YES)
    tab3_lbl_attend_type = Label(tab3_fm2, width=12, font=('Arial', 16), textvariable=sv_attend_type).pack(side=TOP, fill=BOTH, expand=YES)
    tab3_fm2.pack(side=LEFT, padx=10)

    tab3_fm3 = Frame(tab3)
    tab3_lbl_uid = Label(tab3_fm3, width=6, font=('Arial', 12), textvariable=sv_uid).pack(side=TOP, anchor=W, fill=X, expand=YES)
    tab3_btn1 = Button(tab3_fm3, text='Pair', font=('Arial', 10))
    #tab3_btn1.pack(side=TOP, anchor=W, expand=YES)
    tab3_btn1.pack(side=LEFT, anchor=W)
    #tab3_btn1.bind('<Button-1>', tabbar.pair_uid)
    tab3_lbl_pair_status = Label(tab3_fm3, width=1, font=('Arial', 10), textvariable=sv_pair_status).pack(side=LEFT, fill=BOTH, expand=YES)
    tab3_btn2 = Button(tab3_fm3, text='Unpair', font=('Arial', 10))
    tab3_btn2.pack(side=LEFT, anchor=E)
    #tab3_btn2.bind('<Button-1>', tabbar.unpair_uid)
    tab3_fm3.pack(side=LEFT, fill=BOTH, expand=YES)


    # tab4
    tab4 = Tab(root, TAB4)


    tabbar.add(tab1)                   # add the tabs to the tab bar
    tabbar.add(tab2)
    tabbar.add(tab3)
    tabbar.add(tab4)

    #bar.config(bd=2, relief=RIDGE)         # add some border

    tabbar.show()

    root.mainloop()

