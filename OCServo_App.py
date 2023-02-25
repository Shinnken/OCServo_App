import tkinter as tk
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

        entp = tk.StringVar(self.root, value='0')
        entb = tk.StringVar(self.root, value='0')

        #################### WINDOW SETUP END ####################

###################################SERIAL######################################

        serial_frame = tk.Frame(self.root, width=150, height = 100, highlightbackground="black", highlightthickness=1, bg=bcg)
        serial_frame.pack_propagate(0)

        plq = tk.Entry(self.root, textvariable=entp, width=3, bg=blu)
        b_open = tk.Button(serial_frame, text="OPEN", command=self.openSerial, bg="#E376AD")
        b_close = tk.Button(serial_frame, text="CLOSE", command=self.test1, bg="#E376AD")


################# Serial Dropdown Menu ####################
        botmodes = ["COM1", "COM2", "COM3"]
        #botmodes = serial_ports()
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
        for (txt, val) in writeoptions.items(): 
	        tk.Radiobutton(radioframe, text=txt, variable=v, value=val).pack(side = TOP, ipady = 4) 

        radiobut1 = tk.Radiobutton(radioframe, writeoptions, text="Position", variable=writeoption, bg=bcg)


###################################PACKING######################################


        tk.Label(serial_frame, text="Pick Serial Port", bg=bcg).pack()
        dropbotmode.pack()
        serial_frame.pack(pady=5)
        b_open.pack(side=tk.LEFT, padx=5)
        b_close.pack(side=tk.RIGHT, padx=5)
        tk.Label(writeframe, text="Servo Write", bg=bcg).pack()
        writeframe.pack()
        radioframe.pack(pady=5)
        radiobut1.pack(side=tk.LEFT, padx=5)


        plq.pack()################################
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
        self.serial.write(b'\xff\xff\x11\x04\x02\x08\x01\xe5')
        self.serial.read(7)
        



