# Run tkinter code in another thread

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

class App():

    def __init__(self):
        self.inputdata = ""
        self.root = tk.Tk()


    def run(self):
        ####################
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('OCServoTest')

        #####KOLORY#####
        # image2 =tk.PhotoImage('image.jpg')
        bcg = "#16bfe0"
        men = "#eccc1f"
        blu = "#6cb4de"
        m_filter = ""

        try:
            self.root.iconbitmap("301726687_411860101044630_1324108483607034309_n.ico")
        except:
            pass

        self.root.geometry("400x600")
        self.root.config(bg=bcg)

        entp = tk.StringVar(self.root, value='0')
        entb = tk.StringVar(self.root, value='0')


        plq = tk.Entry(self.root, textvariable=entp, width=3, bg=blu)

        botmodes = ["COM1", "COM2", "COM3"]
        # botmodes = serial_ports()
        clickedb = tk.StringVar()
        clickedb.set("Pick COM")
        print(botmodes)

        test = "xd"

        dropbotmode = tk.OptionMenu(self.root, clickedb, *botmodes, command=self.getlabelb)
        dropbotmode.config(bg=men)


        button_frame = tk.Frame(self.root)

        b_episode = tk.Button(button_frame, text="EPISODE", command=self.test1, bg="#E376AD")
        b_single = tk.Button(button_frame, text="SINGLE", command=self.test1, bg="#E376AD")


###################################PACKING######################################


        tk.Label(self.root, text="Placeholder", bg=bcg).pack()
        plq.pack()
        tk.Label(self.root, text="Placeholder", bg=bcg).pack()
        dropbotmode.pack()
        b_episode.pack(side=tk.LEFT)
        b_single.pack(side=tk.RIGHT)
        button_frame.pack(pady=5)



###################################PACKINGEND###################################

        self.root.mainloop()
        
        #######################
    def callback(self):
        self.root.quit()

    def getlabelb(self, selection):
        self.inputdata = selection

    def test1(self):
        print(self.inputdata)

