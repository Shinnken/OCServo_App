import tkinter as tk
from tkinter import ttk
import OCSerial as ocs
from OCSerial import serial_ports



class App():

    def __init__(self):
        self.inputdata = ""
        self.root = tk.Tk()


    def run(self):
        #################### WINDOW SETUP ####################
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('OCServoTest')
        #####KOLORY#####
        # image2 =tk.PhotoImage('image.jpg')
        bcg = "#16bfe0"
        men = "#eccc1f"
        blu = "#6cb4de"

        try:
            self.root.iconbitmap("301726687_411860101044630_1324108483607034309_n.ico")
        except:
            pass

        self.root.geometry("400x600")
        self.root.config(bg=bcg)

        self.entid = tk.IntVar(self.root, value='0')
        self.entpos = tk.IntVar(self.root, value='0')
        self.entspd = tk.IntVar(self.root, value='0')

        #################### WINDOW SETUP END ####################

###################################SERIAL######################################

        serial_frame = tk.Frame(self.root, width=150, height = 100, highlightbackground="black", highlightthickness=1, bg=bcg)
        serial_frame.pack_propagate(0)

        b_open = tk.Button(serial_frame, text="OPEN", command=self.openSerial, bg="#E376AD")
        b_close = tk.Button(serial_frame, text="CLOSE", command=self.test1, bg="#E376AD")


################# Serial Dropdown Menu ####################
        #botmodes = ["COM1", "COM2", "COM3"]
        botmodes = serial_ports()
        clickedb = tk.StringVar()
        clickedb.set("Pick COM")
        print(botmodes)
        dropbotmode = tk.OptionMenu(serial_frame, clickedb, *botmodes, command=self.getlabelb)
        dropbotmode.config(bg=men)
################# Serial Dropdown Menu END ####################

        writeframe = tk.Frame(self.root, width=360, height = 200, highlightbackground="black", highlightthickness=1, bg=bcg)
        writeframe.pack_propagate(0)
        radioframe = tk.Frame(writeframe, bg=bcg)
        writeoptions = {"Write": 0, "Sync Write": 1, "Bulk Write": 2, "Reg Write": 3}
        writeoption = tk.IntVar()
        x = 0
        rbutton = [None, None, None, None]
        for (txt, val) in writeoptions.items():
            rbutton[x] = tk.Radiobutton(radioframe, text=txt, variable=writeoption, value=val, bg=bcg)
            x += 1

        w = 7
        entryframe = tk.Frame(writeframe, bg=bcg)
        idframe = tk.Frame(entryframe)
        identry = tk.Entry(idframe, textvariable=self.entid, width=w, bg=blu)
        posframe = tk.Frame(entryframe)
        posentry = tk.Entry(posframe, textvariable=self.entpos, width=w, bg=blu)
        spdframe = tk.Frame(entryframe)
        spdentry = tk.Entry(spdframe, textvariable=self.entspd, width=w, bg=blu)
        b_send = tk.Button(writeframe, text="SEND", command=self.send, bg="#E376AD")


        #radiobut1 = tk.Radiobutton(radioframe, writeoptions, text="Position", variable=writeoption, bg=bcg)


###################################PACKING######################################


        tk.Label(serial_frame, text="Pick Serial Port", bg=bcg).pack()
        dropbotmode.pack()
        serial_frame.pack(pady=5)
        b_open.pack(side=tk.LEFT, padx=5)
        b_close.pack(side=tk.RIGHT, padx=5)
        tk.Label(writeframe, text="Servo Write", bg=bcg).pack()
        writeframe.pack()
        radioframe.pack(pady=5)
        for i in range(4):
            rbutton[i].config(activebackground=bcg)
            rbutton[i].pack(side=tk.LEFT, padx=5)
        ttk.Separator(writeframe, style='red.TSeparator').pack(fill=tk.X, pady=5)
        tk.Label(writeframe, text="Input Values", bg=bcg).pack()
        entryframe.pack(side=tk.TOP)
        tk.Label(idframe, text="Servo ID: ", bg=bcg).pack(side=tk.LEFT)
        identry.pack(side=tk.RIGHT)
        idframe.pack(side=tk.LEFT)
        tk.Label(posframe, text="Servo POS: ", bg=bcg).pack(side=tk.LEFT)
        posentry.pack(side=tk.RIGHT)
        posframe.pack(side=tk.LEFT)
        tk.Label(spdframe, text="Servo SPD: ", bg=bcg).pack(side=tk.LEFT)
        spdentry.pack(side=tk.RIGHT)
        spdframe.pack(side=tk.LEFT)
        b_send.pack(anchor=tk.SE, padx=5, pady=5)

        ################################


###################################PACKINGEND###################################

        self.root.mainloop()
        
        #######################
        #   END OF MAINLOOP   #


    def callback(self):
        self.root.quit()
        self.serial.callback()

    def getlabelb(self, selection):
        self.inputdata = selection

    def openSerial(self):
        self.serial = ocs.OCSerial()
        self.serial.port = self.inputdata
        self.serial.start()
        print(self.inputdata)

    def test1(self):
        self.serial.write(b'\xff\xff\x11\x04\x02\x02\x01\xe5')
        self.serial.read(7)
        self.serial.write(b'\xff\xff\x11\x04\x02\x08\x01\xdf')
        self.serial.read(7)
        self.serial.write(b'\xff\xff\x11\x04\x02\x08\x01\xdf')
        self.serial.read(7)

# Checksum function, returns the checksum of the data, if sum is greater than 255, take the lowest 8 bits and then invert
    def checksum(self, data):
        sum = 0
        for i in range(2, len(data)-1):
            sum += data[i]
        if sum > 255:
            sum = sum & 0xff
        return ~sum & 0xff

    def write(self, servoid, pos):
        datalength = 5
        instruction = 0x03
        address = 0x2a
        pos = pos.to_bytes(2, 'little')
        data = bytearray([0xff, 0xff, servoid, datalength, instruction, address, pos[0], pos[1]])
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(15)

    def send(self):
        self.write(self.entid.get(), self.entpos.get())

