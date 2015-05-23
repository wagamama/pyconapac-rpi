#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################
# Tabbed interface script
# www.sunjay-varma.com
###################################################

from Tkinter import *
import csv
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
TAB4 = u"同步".encode('utf-8')
TAB5 = "EXIT"
NOT_FOUND = "NOT FOUND"

BASE = RAISED
SELECTED = FLAT

# a base tab class
class Tab(Frame, threading.Thread):
    def __init__(self, master, name):
        Frame.__init__(self, master)
        self.tab_name = name


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

    def run(self):
        global conn
        conn = sqlite3.connect(DB_NAME)
        conn.isolation_level = None

	while True:
			
            time.sleep(0.5)
            print self.current_tab

            if self.current_tab == TAB1 :
                                
                p = subprocess.Popen('/home/pi/nfc/libnfc-1.7.0-rc7/examples/nfc-poll', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in p.stdout.readlines():
		    if "UID (NFCID1)" in line:
                        uid_nfcid = line.split(":")
                        uid = uid_nfcid[1].strip(' \t\n\r')

                        cursor = conn.cursor()
                        cursor.execute('''SELECT reg_no, uid, fullname, nickname, attend_type, regist_wtime FROM regist WHERE uid=?''', (uid,))
                        all_rows = cursor.fetchall()

                        if len(all_rows) == 0:
                            sv_reg_no.set("")
                            sv_nickname.set("NOT FOUND!!")
                            sv_attend_type.set("")
                            root.update_idletasks()
			else:
                            for row in all_rows:
                                print row[0], row[2], row[3], row[4], row[5]
                                reg_no_var = row[0]
                                fullname_var = row[2]
                                nickname_var = row[3]
                                attend_type_var = row[4]
                                regist_wtime_var = row[5]
                                sv_reg_no.set(reg_no_var)
                                sv_nickname.set(nickname_var)
                                sv_attend_type.set(attend_type_var)
                                sv_uid.set(uid)
                                sv_regist_status.set(row[5])
                                root.update_idletasks()

                	if self.current_tab == TAB3 :
				global uid_var
				#global reg_no_var

				reg_no_var = int(txt3_fm1.get(1.0, END))
				#global conn
				conn = sqlite3.connect(DB_NAME)
				conn.isolation_level = None

				cursor = conn.cursor()
				cursor.execute('''SELECT uid, fullname, nickname, attend_type, regist_wtime FROM regist WHERE reg_no=?''', (reg_no_var,))
				all_rows = cursor.fetchall()

				retval = p.wait()
				time.sleep(1)
		

	
	def show(self):
		self.pack(side=TOP, expand=YES, fill=X)
		self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
	
	def add(self, tab):
		tab.pack_forget()									# hide the tab on init
		
		self.tabs[tab.tab_name] = tab						# add it to the list of tabs
		b = Button(self, text=tab.tab_name, relief=BASE,	# basic button stuff
			command=(lambda name=tab.tab_name: self.switch_tab(name)))	# set the command to switch tabs
		b.pack(side=LEFT)												# pack the buttont to the left mose of self
		self.buttons[tab.tab_name] = b											# add it to the list of buttons
	
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
			self.tabs[self.current_tab].pack_forget()			# hide the current tab
		self.tabs[name].pack(side=BOTTOM)							# add the new tab to the display
		self.current_tab = name									# set the current tab to itself
		
		self.buttons[name].config(relief=SELECTED)					# set it to the selected style

                if self.current_tab == TAB1 :
                        self.winfo_toplevel().wm_geometry("320x240+0+0")
                        #root.wm_overrideredirect(True)
                        subprocess.call(['/home/pi/sh/kill_keyboard.sh'])
			sv_reg_no.set("")
			sv_nickname.set("")
			sv_attend_type.set("")
			root.update_idletasks()

                if self.current_tab == TAB2 :
                        self.winfo_toplevel().wm_geometry("320x240+0+0")
                        subprocess.call(['/home/pi/sh/kill_keyboard.sh'])
			sv_reg_no.set("")
			sv_nickname.set("")
			sv_attend_type.set("")
			root.update_idletasks()

                if self.current_tab == TAB3 :
                        #root.wm_overrideredirect(True)
                        self.winfo_toplevel().wm_geometry("320x100+0+100")
                        #self.winfo_toplevel().wm_geometry("320x240+0+0")
                        subprocess.call(['/home/pi/sh/matchbox_keyboard_numpad.sh'])
			sv_reg_no.set("")
			sv_nickname.set("")
			sv_attend_type.set("")
			root.update_idletasks()

                #if self.current_tab == TAB4 :
                #        subprocess.call(['/home/pi/sh/kill_keyboard.sh'])
                #        subprocess.call(['sudo', '/home/pi/sh/kill_touch.sh'])

                if self.current_tab == TAB5 :
                        subprocess.call(['/home/pi/sh/kill_keyboard.sh'])
                        subprocess.call(['sudo', '/home/pi/sh/kill_touch.sh'])


	def load_profile(self, event):
		print "load_profile"
		global uid_var
		global reg_no_var

		reg_no_var = int(txt3_fm1.get(1.0, END))
		#global conn
		conn = sqlite3.connect(DB_NAME)
		conn.isolation_level = None

	        cursor = conn.cursor()
                cursor.execute('''SELECT uid, fullname, nickname, attend_type, regist_wtime FROM regist WHERE reg_no=?''', (reg_no_var,))
		all_rows = cursor.fetchall()

		if len(all_rows) == 0:
			cmd = 'echo ' + NOT_FOUND + ' >> /tmp/regist_log'
			os.popen(cmd)

                        sv_reg_no.set("")
                        sv_reg_no.set(NOT_FOUND)
                        sv_nickname.set("")
                        #attend_type.set(attend_type_var.encode('utf-8'))
		        sv_uid.set("")
		        sv_pair_status.set("")
			print NOT_FOUND
			root.update_idletasks()
                else:
                        for row in all_rows:
				root.update_idletasks()
				uid_var = row[0]
                            	fullname_var = row[1]
                            	nickname_var = row[2]
                            	attend_type_var = row[3]
                            	regist_wtime_var = row[4]

				cmd = 'echo ' + nickname_var + ' >> /tmp/regist_log'
				os.popen(cmd)

				print row[0], row[1], row[2], row[3], row[4]

                                sv_reg_no.set("")
                                sv_reg_no.set(reg_no_var)
                                sv_nickname.set(nickname_var.encode('utf-8'))
                                #regist_wtime.set(regist_wtime.encode('utf-8'))
                            	#attend_type.set(attend_type_var.encode('utf-8'))
				sv_uid.set("")
				sv_pair_status.set("")

				root.update_idletasks()

		            	p = subprocess.Popen('/home/pi/nfc/libnfc-1.7.0-rc7/examples/nfc-poll', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            			for line in p.stdout.readlines():
                			print line

                			if "UID (NFCID1)" in line:
						uid_nfcid = line.split(":")
                    				uid_var = uid_nfcid[1].strip(' \t\n\r')
						sv_uid.set(uid_var)
						root.update_idletasks()

            		retval = p.wait()
            		time.sleep(1)







	def pair_uid(self, event):
		print "update_uid"
		print uid_var

		conn = sqlite3.connect(DB_NAME)
		conn.isolation_level = None

	        cursor = conn.cursor()
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		cursor.execute('''UPDATE regist SET regist_wtime =?, uid=? WHERE reg_no=?''', (now, uid_var, reg_no_var,))

	        #cursor = conn.cursor()
                #cursor.execute('''SELECT uid, fullname, nickname, attend_type, regist_wtime FROM regist WHERE reg_no=?''', (reg_no_var,))
		sv_pair_status.set("P")

		print "pair ok"

	def unpair_uid(self, event):
		print "cancel_update"
		print "update_uid"
		#print uid_var

		conn = sqlite3.connect(DB_NAME)
		conn.isolation_level = None

		uid_var = ""
	        cursor = conn.cursor()
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		cursor.execute('''UPDATE regist SET regist_wtime =?, uid=? WHERE reg_no=?''', (now, uid_var, reg_no_var,))

		sv_uid.set("")
		sv_pair_status.set("U")

		print "unpair ok"


def run_command(command):
	p = subprocess.Popen(command,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT)
	return iter(p.stdout.readline, b'')


def get_ip():
	ip = ""
	cmd = '/home/pi/sh/ip.sh'
	for line in run_command(cmd):
		ip += line.strip(' \t\n\r')
	return ip

			
if __name__ == '__main__':
	def write(x): print x
		
	root = Tk()
	ip = get_ip()
	root.title(ip)
        #root.geometry('320x240+0+0') 
        #root.geometry('0+0') 
        #root.resizable(0,0)


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
	#txt3_fm1 = StringVar()


	tabbar = TabBar(root, TAB1)
	
	# tab1
	tab1 = Tab(root, TAB1)

        tab1_lbl_reg_no = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_nickname = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_nickname).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_attend_type = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_attend_type).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_uid = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_uid).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_regist_status = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_regist_status).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_regist_count = Label(tab1, width=50, height=1, font=('Arial', 16), textvariable=sv_regist_count).pack(side=TOP, expand=YES, fill=BOTH)


	# tab2	
	tab2 = Tab(root, TAB2)
	#Label(tab2, text="How are you??", bg='black', fg='#3366ff').pack(side=TOP, fill=BOTH, expand=YES)
	#txt = Text(tab2, width=50, height=20)
	#txt.focus()
	#txt.pack(side=LEFT, fill=X, expand=YES)
    	#:Button(tab2, text="Get", command=(lambda: write(txt.get('1.0', END).strip()))).pack(side=BOTTOM, expand=YES, fill=BOTH)

        tab1_lbl_reg_no = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_reg_no).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_nickname = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_nickname).pack(side=TOP, expand=YES, fill=BOTH)
        tab1_lbl_attend_type = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_attend_type).pack(side=TOP, expand=YES, fill=BOTH)
        #tab1_lbl_tshirt_size = Label(tab2, width=50, height=1, font=('Arial', 16), textvariable=sv_tshirt_size).pack(side=TOP, expand=YES, fill=BOTH)
	txt = Text(tab2, width=50, height=20)
	txt.pack(side=LEFT, fill=X, expand=YES)
	
	# tab3
	tab3 = Tab(root, TAB3)
	tab3_fm1 = Frame(tab3)
        txt3_fm1 = Text(tab3_fm1, width=3, height=1, font=('Arial', 12))
        txt3_fm1.pack(side=TOP, fill=X, expand=YES)
        txt3_fm1.focus()
	tab3_btn1 = Button(tab3_fm1, text='OK')
	tab3_btn1.pack(side=TOP, anchor=W, fill=X, expand=YES)
	tab3_btn1.bind('<Button-1>', tabbar.load_profile)
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
	tab3_btn1.bind('<Button-1>', tabbar.pair_uid)
	tab3_lbl_pair_status = Label(tab3_fm3, width=1, font=('Arial', 10), textvariable=sv_pair_status).pack(side=LEFT, fill=BOTH, expand=YES)
	tab3_btn2 = Button(tab3_fm3, text='Unpair', font=('Arial', 10))
	tab3_btn2.pack(side=LEFT, anchor=E)
	tab3_btn2.bind('<Button-1>', tabbar.unpair_uid)
	tab3_fm3.pack(side=LEFT, fill=BOTH, expand=YES)

	#Button(tab1, text='Hello').pack(side=LEFT, fill=Y)
	#Label(tab1,  text='Hello container world').pack(side=TOP)
	#Button(tab1, text='Quit').pack(side=RIGHT, expand=YES,fill=X)


        # tab4
        tab4 = Tab(root, TAB4)

        # tab5
        tab5 = Tab(root, TAB5)

        root.update_idletasks()
        tabbar.add(tab1)                   # add the tabs to the tab bar
        tabbar.add(tab2)
        tabbar.add(tab3)
        tabbar.add(tab4)
        tabbar.add(tab5)


	#tabbar.config(bd=2, relief=RIDGE)			# add some border
	
	tabbar.show()
	
	root.mainloop()
