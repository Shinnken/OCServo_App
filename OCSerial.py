# Run tkinter code in another thread

import tkinter as tk
import threading
import serial
import sys
import glob

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



class OCSerial(threading.Thread):

    def __init__(self):
        self.inputdata = ""
        self.port = ""
        self.root = tk.Tk()
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.serialPort = serial.Serial(self.port, 1_000_000, timeout=1)   # open serial port

    def write(self, data):
        self.serialPort.write(data)
        print("Wrote: " + str(data))

    def read(self, bytes_to_read=1):
        print("Reading: " + hex(bytes_to_read))
        return self.serialPort.read(bytes_to_read)

    def callback(self):
        self.serialPort.close()
        self.root.quit()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

