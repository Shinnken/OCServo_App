import tkinter as tk
from tkinter import ttk
import OCSerial as ocs
from OCSerial import serial_ports
import time

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        s = ttk.Style()
        s.configure('new.TFrame', background='#16bfe0')
        canvas = tk.Canvas(self, bg="#16bfe0")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='new.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class App:
    def __init__(self):
        self.inputdata = ""
        self.root = tk.Tk()
        self.serial = ocs.OCSerial()
        self.serial.join()
        self.n = 8


    def run(self):
        #################### WINDOW SETUP ####################
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('OCServoTest')
        #####KOLORY#####
        # image2 =tk.PhotoImage('image.jpg')
        self.bcg = "#16bfe0"
        self.men = "#eccc1f"
        self.blu = "#6cb4de"

        try:
            self.root.iconbitmap("301726687_411860101044630_1324108483607034309_n.ico")
        except:
            pass

        #self.root.geometry("400x600")
        self.root.geometry("500x600")
        self.root.config(bg=self.bcg)


        self.scrollable = ScrollableFrame(self.root)
        self.scrollable.pack(fill="both", expand=True)

        self.entid = []
        self.entpos = []
        self.entspd = []
        self.entfilename = tk.StringVar()
        for i in range(self.n):
            self.entid.append(tk.IntVar(self.scrollable.scrollable_frame, value=10+i))
            self.entpos.append(tk.IntVar(self.scrollable.scrollable_frame, value=2047))
            self.entspd.append(tk.IntVar(self.scrollable.scrollable_frame, value=0))


        #################### WINDOW SETUP END ####################

###################################SERIAL######################################

        serial_frame = tk.Frame(self.scrollable.scrollable_frame, width=150, height=100, highlightbackground="black", highlightthickness=1, bg=self.bcg)
        serial_frame.pack_propagate(0)

        b_open = tk.Button(serial_frame, text="OPEN", command=self.openSerial, bg="#E376AD")
        b_close = tk.Button(serial_frame, text="CLOSE", command=self.closeSerial, bg="#E376AD")


################# Serial Dropdown Menu ####################
        #botmodes = ["COM1", "COM2", "COM3"]
        botmodes = serial_ports()
        clickedb = tk.StringVar()
        clickedb.set("Pick COM")
        print(botmodes)
        dropbotmode = tk.OptionMenu(serial_frame, clickedb, *botmodes, command=self.getlabelb)
        dropbotmode.config(bg=self.men)
################# Serial Dropdown Menu END ####################

        self.writeframe = tk.Frame(self.scrollable.scrollable_frame, width=460, height=350, highlightbackground="black", highlightthickness=1, bg=self.bcg)
        self.writeframe.pack_propagate(0)
        radioframe = tk.Frame(self.writeframe, bg=self.bcg)
        writeoptions = {"Write": 0, "Sync Write": 1, "Bulk Write": 2, "Reg Write": 3}
        self.writeoption = tk.IntVar()
        x = 0
        rbutton = [None, None, None, None]
        for (txt, val) in writeoptions.items():
            rbutton[x] = tk.Radiobutton(radioframe, text=txt, variable=self.writeoption, value=val, bg=self.bcg, command=self.servowriteoption)
            x += 1
        self.entryframe = tk.Frame(self.writeframe, bg=self.bcg)
        self.b_send = tk.Button(self.writeframe, text="SEND", command=self.send, bg="#E376AD")
        self.b_read = tk.Button(self.writeframe, text="READ", command=self.read, bg="#E376AD")
        self.b_on = tk.Button(self.scrollable.scrollable_frame, text="ON", command=self.on, bg="#E376AD")
        self.b_off = tk.Button(self.scrollable.scrollable_frame, text="OFF", command=self.off, bg="#E376AD")
        self.b_offfeet = tk.Button(self.scrollable.scrollable_frame, text="FEET OFF", command=self.offfeet, bg="#E376AD")
        self.b_offleg1 = tk.Button(self.scrollable.scrollable_frame, text="R LEG OFF", command=self.offlegr, bg="#E376AD")
        self.b_offleg2 = tk.Button(self.scrollable.scrollable_frame, text="L LEG OFF", command=self.offlegl, bg="#E376AD")
        self.exportframe = tk.Frame(self.scrollable.scrollable_frame, highlightbackground="black", highlightthickness=1, bg=self.bcg)
        self.b_export = tk.Button(self.exportframe, text="EXPORT", command=self.exportpos, bg="#E376AD")
        self.b_import = tk.Button(self.exportframe, text="IMPORT", command=self.importpos, bg="#E376AD")
        self.filenameentry = tk.Entry(self.exportframe, textvariable=self.entfilename, width=5, bg=self.blu)

        #radiobut1 = tk.Radiobutton(radioframe, writeoptions, text="Position", variable=writeoption, bg=self.bcg)


###################################PACKING######################################


        tk.Label(serial_frame, text="Pick Serial Port", bg=self.bcg).pack()
        dropbotmode.pack()
        serial_frame.pack(pady=5)
        b_open.pack(side=tk.LEFT, padx=5)
        b_close.pack(side=tk.RIGHT, padx=5)
        tk.Label(self.writeframe, text="Servo Write", bg=self.bcg).pack()
        self.writeframe.pack()
        radioframe.pack(pady=5)
        for i in range(4):
            rbutton[i].config(activebackground=self.bcg)
            rbutton[i].pack(side=tk.LEFT, padx=5)
        rbutton[self.writeoption.get()].invoke()
        ttk.Separator(self.writeframe, style='red.TSeparator').pack(fill=tk.X, pady=5)

############################### Write Options ##################################

        #self.write()
        tk.Label(self.writeframe, text="Input Values", bg=self.bcg).pack()

        self.entryframe.pack(side=tk.TOP, fill=tk.X)

        self.b_send.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)
        self.b_read.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)
        self.exportframe.pack(pady=5)
        self.filenameentry.pack(side=tk.LEFT, padx=5)
        self.b_export.pack(side=tk.LEFT, padx=5)
        self.b_import.pack(side=tk.LEFT, padx=5)
        self.b_on.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=5)
        self.b_off.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=5)
        self.b_offfeet.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=5)
        self.b_offleg2.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=5)
        self.b_offleg1.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=5)
        ################################


###################################PACKINGEND###################################

        self.root.mainloop()

        #######################
        #   END OF MAINLOOP   #


    def getlabelb(self, selection):
        self.inputdata = selection

    def openSerial(self):
        self.serial.port = self.inputdata
        self.serial.start()
        print(self.inputdata)

    def closeSerial(self):
        self.serial.callback()
    def callback(self):
        try:
            self.root.quit()
            self.serial.callback()
        except:
            self.root.quit()


# Checksum function, returns the checksum of the data, if sum is greater than 255, take the lowest 8 bits and then invert
    def checksum(self, data):
        sum = 0
        for i in range(2, len(data)):
            sum += data[i]
        if sum > 255:
            sum = sum & 0xff
        #print(sum)
        return ~sum & 0xff
    def test1(self):
        self.serial.write(b'\xff\xff\x11\x04\x02\x02\x01\xe5')
        self.serial.read(7)
        self.serial.write(b'\xff\xff\x11\x04\x02\x08\x01\xdf')
        self.serial.read(7)
        test = bytearray([0xff, 0xff, 0x11, 0x04, 0x02, 0x08, 0x01])
        print(test[2:])
        test.append(self.checksum(test))
        self.serial.write(test)
        self.serial.read(7)

    def servowrite(self, servoid, pos,):
        datalength = 0
        instruction = 0x03
        address = 0x2a
        pos = pos.to_bytes(2, 'little')
        data = bytearray([0xff, 0xff, servoid, datalength, instruction, address, pos[0], pos[1], 0xe8, 0x06])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(15)

    def servoread(self, servoid):
        datalength = 0
        instruction = 0x02
        address = [0x39, 0x38]
        data = bytearray([0xff, 0xff, servoid, datalength, instruction, address[1], address[0]])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        message = self.serial.read(34)
        #print(message)
        value = message[5] | message[6] << 8
        return value

    def syncsend(self):
        datalength = 0
        instruction = 0x83
        address = 0x2a
        length = 0x04
        data = bytearray([0xff, 0xff, 0xfe, datalength, instruction, address, length])
        for i in range(len(self.entid)):
            pos = self.entpos[i].get().to_bytes(2, 'little')
            spd = self.entspd[i].get().to_bytes(2, 'little')
            data.append(self.entid[i].get())
            data.append(pos[0])
            data.append(pos[1])
            data.append(spd[0])
            data.append(spd[1])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(25)


    def send(self, num=0):
        self.servowrite(self.entid[num].get(), self.entpos[num].get())
        self.serial.value = self.entid[num].get()

    def write(self, num=0):
        w = 7
        self.servoframe = tk.Frame(self.entryframe, bg=self.bcg)
        idframe = tk.Frame(self.servoframe, bg=self.bcg)
        identry = tk.Entry(idframe, textvariable=self.entid[num], width=w, bg=self.blu)
        posframe = tk.Frame(self.servoframe, bg=self.bcg)
        posentry = tk.Entry(posframe, textvariable=self.entpos[num], width=w, bg=self.blu)
        spdframe = tk.Frame(self.servoframe, bg=self.bcg)
        spdentry = tk.Entry(spdframe, textvariable=self.entspd[num], width=w, bg=self.blu)
        #####################################################################################
        tk.Label(idframe, text="Servo ID: ", bg=self.bcg).pack(side=tk.LEFT)
        self.servoframe.pack(side=tk.TOP, fill=tk.X)
        identry.pack(side=tk.RIGHT)
        idframe.pack(side=tk.LEFT)
        tk.Label(posframe, text="Servo POS: ", bg=self.bcg).pack(side=tk.LEFT)
        posentry.pack(side=tk.RIGHT)
        posframe.pack(side=tk.LEFT)
        tk.Label(spdframe, text="Servo OT(ms): ", bg=self.bcg).pack(side=tk.LEFT)
        spdentry.pack(side=tk.RIGHT)
        spdframe.pack(side=tk.LEFT)



    def servowriteoption(self):
        self.clearframe()
        if self.writeoption.get() == 0:
            self.b_send.config(command=self.send)
            self.write()
        elif self.writeoption.get() == 1:
            self.b_send.config(command=self.syncsend)
            self.syncwrite()

    def clearframe(self):
        for widget in self.entryframe.winfo_children():
            widget.destroy()

    def syncwrite(self):
        for i in range(self.n):
            self.write(i)


    def read(self):
        for i in range(len(self.entid)):
            self.entpos[i].set(self.servoread(self.entid[i].get()))
            print("Servo %d: %d" % (self.entid[i].get(), self.entpos[i].get()))
        #self.servoread(self.entid[0].get())

    def on(self):
        datalength = 0
        instruction = 0x03
        address = 0x28
        data = bytearray([0xff, 0xff, 0xfe, datalength, instruction, address, 0x01])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)

    def off(self):
        datalength = 0
        instruction = 0x03
        address = 0x28
        data = bytearray([0xff, 0xff, 0xfe, datalength, instruction, address, 0x00])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)

    def offfeet(self):
        datalength = 0
        instruction = 0x03
        address = 0x28
        data = bytearray([0xff, 0xff, 0x10, datalength, instruction, address, 0x00])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(25)
        data[2] = 0x11
        data[-1] = self.checksum(data[:-1])
        self.serial.write(data)
        self.serial.read(25)

    def offlegr(self):
        datalength = 0
        instruction = 0x03
        address = 0x28
        data = bytearray([0xff, 0xff, 0x0a, datalength, instruction, address, 0x00])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(25)
        for i in range(3):
            data[2] = (2*i)+12
            data[-1] = self.checksum(data[:-1])
            self.serial.write(data)

    def offlegl(self):
        datalength = 0
        instruction = 0x03
        address = 0x28
        data = bytearray([0xff, 0xff, 0x0b, datalength, instruction, address, 0x00])
        data[3] = len(data) - 3
        data.append(self.checksum(data))
        self.serial.write(data)
        self.serial.read(25)
        for i in range(3):
            data[2] = (2*i)+13
            data[-1] = self.checksum(data[:-1])
            self.serial.write(data)

    def exportpos(self):
        filename = self.entfilename.get() + '.txt'
        with open(filename, 'w') as f:
            for i in range(len(self.entid)):
                f.write("%d %d\n" % (self.entid[i].get(), self.entpos[i].get()))
            f.close()

    def importpos(self):
        filename = self.entfilename.get() + '.txt'
        with open(filename, 'r') as f:
            for i in range(len(self.entid)):
                line = f.readline().split()
                self.entid[i].set(int(line[0]))
                self.entpos[i].set(int(line[1]))
            f.close()

