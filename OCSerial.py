# Run tkinter code in another thread

import tkinter as tk
import threading
import sys
import glob
import serial



class OCSerial(threading.Thread):

    def __init__(self):
        self.inputdata = ""
        self.root = tk.Tk()
        threading.Thread.__init__(self)
        self.start()

    def run(self,com):
        self.port = serial.Serial(com)


    def callback(self):
        self.port.close()
        self.root.quit()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

