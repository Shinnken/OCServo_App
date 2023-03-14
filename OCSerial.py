# Run tkinter code in another thread

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
    print(ports)
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            print()
            pass
    return result



class OCSerial(threading.Thread):

    def __init__(self):
        self.inputdata = ""
        self.port = ""
        threading.Thread.__init__(self)

    def run(self):
        self.serialPort = serial.Serial(self.port, 1_000_000, timeout=1)   # open serial port


    # def write(self, data):
    #     self.serialPort.write(data)
    #     hex_data = ' '.join(hex(b)[2:].zfill(2) for b in data)
    #     print(f"Wrote: {hex_data}")


    def read(self, bytes_to_read=1):
        msg = self.serialPort.read(bytes_to_read)
        data = msg.hex('/')
        print("Reading: " + str(data))
        return msg

    def read(self, bytes_to_read=1):
        msg = self.serialPort.read(bytes_to_read)
        data = '/'.join([hex(b)[2:].zfill(2) for b in msg])
        print("Reading: " + str(data))
        return msg

    def callback(self):
        self.serialPort.close()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

