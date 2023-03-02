# Run tkinter code in another thread

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


def checksum(data):
    sum = 0
    for i in range(2, len(data)):
        sum += data[i]
    if sum > 255:
        sum = sum & 0xff
    print(sum)
    return ~sum & 0xff

# transform function that converts a given angle -180 to 180 to the 0 to 4095 range
def transform(angle):
    return int((angle + 180) * 4095 / 360)

class OCSerial():

    def __init__(self, port):
        self.inputdata = ""
        self.pos = None
        self.value = 0
        self.serialPort = serial.Serial(port, 1_000_000, timeout=1)

    def write(self, data):
        self.serialPort.write(data)
        hex_data = ' '.join(hex(b)[2:].zfill(2) for b in data)
        print(f"Wrote: {hex_data}")


    def read(self, bytes_to_read=1):
        msg = self.serialPort.read(bytes_to_read)
        data = msg.hex(sep='/')
        print("Reading: " + str(data))
        return msg

    def callback(self):
        self.serialPort.close()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

    def send(self, id, angle):
        datalength = 0
        instruction = 0x03
        address = 0x2a
        pos = transform(angle).to_bytes(2, 'little')
        data = bytearray([0xff, 0xff, id, datalength, instruction, address, pos[0], pos[1]])
        data[3] = len(data) - 3
        data.append(checksum(data))
        self.write(data)
        self.read(100)

    def syncsend(self, idlist, poslist):
        datalength = 0
        instruction = 0x83
        address = 0x2a
        length = 0x02
        data = bytearray([0xff, 0xff, 0xfe, datalength, instruction, address, length])
        for i in range(len(idlist)):
            pos = poslist[i].to_bytes(2, 'little')
            data.append(idlist[i])
            data.append(pos[0])
            data.append(pos[1])
        data[3] = len(data) - 3
        data.append(checksum(data))
        self.write(data)
