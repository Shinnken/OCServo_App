# Servo Test by Konrad Suchodolski

import os
import tkinter as tk
import sys
import glob
import serial

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


inputdata = ""
def getlabelb(selection):
    global inputdata
    inputdata = selection
def test1():
    print(inputdata)


root = tk.Tk()
root.title('OCServoTest')

#####KOLORY#####
#image2 =tk.PhotoImage('image.jpg')
bcg = "#16bfe0"
men = "#eccc1f"
blu = "#6cb4de"
m_filter = ""

try:
    root.iconbitmap("301726687_411860101044630_1324108483607034309_n.ico")
except:
    pass



root.geometry("400x600")
root.config(bg = bcg)

entp = tk.StringVar(root, value='0')
entb = tk.StringVar(root, value='0')

tk.Label(root, text="Placeholder",bg = bcg).pack()
plq = tk.Entry(root,textvariable=entp, width=3,bg = blu).pack()

botmodes = serial_ports()
clickedb = tk.StringVar()
clickedb.set("Pick COM")


tk.Label(root, text="Placeholder",bg = bcg).pack()
dropbotmode = tk.OptionMenu(root, clickedb, *botmodes,command=getlabelb)
dropbotmode.config(bg = men)
dropbotmode.pack()

button_frame = tk.Frame(root)

b_episode = tk.Button(button_frame, text="EPISODE",command=test1, bg="#E376AD")
b_single = tk.Button(button_frame, text="SINGLE",command=test1, bg="#E376AD")
b_episode.pack(side=tk.LEFT)
b_single.pack(side=tk.RIGHT)
button_frame.pack(pady=5)


root.mainloop()