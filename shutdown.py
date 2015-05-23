# http://goo.gl/xHbKcY
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import os

sudoPassword = 'raspberry'
shutdown_sh = '/home/pi/pyconapac-rpi/sh/shutdown.sh'

class App:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

def onClickOK():
    print "onClickOK()"
    os.system("sudo sync; sudo init 0")

def onClickCancel():
    print "onClickCancel()"
    global root
    root.quit()

root = Tk()
root.geometry('200x160') 
root.resizable(0,0)

mainLabel = Label(root, width=15, height=2, font=('Arial', 16), text='Shutdown Now?')
mainLabel.pack()
okButton   = Button(root, width=5, text='OK', command=onClickOK)
exitButton = Button(root, width=5, text='Cancel', command=onClickCancel)
okButton.pack(padx=15, pady=10, side=LEFT)
exitButton.pack(padx=15, pady=10, side=LEFT)

root.mainloop()
