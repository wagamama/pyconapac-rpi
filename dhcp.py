# http://goo.gl/xHbKcY
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import subprocess

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        ip = ''
        cmd = '/home/pi/pyconapac-rpi/sh/ip.sh'
        for line in self.run_command(cmd):
            ip += line
        var = StringVar()
        var.set(ip)
        lable = Label(master, textvariable = var)
        lable.pack()
        button = Button(master, text="exit", command=(lambda: exit())).pack(side=BOTTOM, fill=BOTH, expand=YES)

    def run_command(self, command):
        p = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    def exit():
        global root
        root.quit()


def sel():
    selection = "Value = " + str(var.get())
    label.config(text = selection)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.geometry("200x160")
    root.mainloop()
