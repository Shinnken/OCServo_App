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

        serial_frame = tk.Frame(self.root)

        plq = tk.Entry(self.root, textvariable=entp, width=3, bg=blu)
        b_open = tk.Button(serial_frame, text="OPEN", command=self.openSerial, bg="#E376AD")
        b_close = tk.Button(serial_frame, text="CLOSE", command=self.test1, bg="#E376AD")


################# Serial Dropdown Menu ####################
        # botmodes = ["COM1", "COM2", "COM3"]
        botmodes = serial_ports()
        clickedb = tk.StringVar()
        clickedb.set("Pick COM")
        print(botmodes)
        dropbotmode = tk.OptionMenu(serial_frame, clickedb, *botmodes, command=self.getlabelb)
        dropbotmode.config(bg=men)
################# Serial Dropdown Menu END ####################

        button_frame = tk.Frame(self.root)




###################################PACKING######################################


        tk.Label(serial_frame, text="Pick Serial Port", bg=bcg).pack()
        dropbotmode.pack()
        serial_frame.pack(pady=5)
        b_open.pack(side=tk.LEFT)
        b_close.pack(side=tk.RIGHT)
        button_frame.pack(pady=5)


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




