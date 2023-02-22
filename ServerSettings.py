import pandas as pd
import os
import tkinter as tk
from socket import getaddrinfo, AF_INET, gethostname, gethostbyname



startserver1 = 'start FGServer.exe -batchmode -disableEAC -disconnectBadConnections false -disconnectNotReadyConnections false -nographics -gameduration 180 '
minplayer = ' -minplayers '
maxplayer = ' -maxplayers '
startserver2 = ' -beginGameImmediately -lobbytimeoutduration 36000000 -logFile "..\Logs\FGServer.log" -NumServerBots '
startserver3 = ' -AIOverride '

killall1 = 'taskkill /fi "IMAGENAME eq FGServer.exe" /im *'
killall2 = 'taskkill /fi "IMAGENAME eq FallGuys_server.exe" /im *'

hostname = gethostname()
local_ip = gethostbyname(hostname)

def gen():
    for ip in getaddrinfo(host=gethostname(), port=None, family=AF_INET):
        yield (ip[4][0])

g = gen()

try:
    ip1 = next(g)
    ip2 = next(g)
except StopIteration:
    ip2 = "None"


# PANDAS
p_maps_single = pd.read_excel("Adding Variations.xlsx", "Variation List")
p_maps_episode = pd.read_excel("Adding Variations.xlsx", "Map List")

maps_single = p_maps_single["Single Episode Name"].tolist()
maps_episode = p_maps_episode["Single Episode Name"].tolist()
all_maps = maps_single + maps_episode
maps = [""]


root = tk.Tk()
root.title('FallGuys Server Settings')

try:
    root.iconbitmap("ServerSettings.exe")
except:
    a=1



#####KOLORY#####
#image2 =tk.PhotoImage('image.jpg')
bcg = "#94d41c"
men = "#eccc1f"
blu = "#6cb4de"
m_filter = ""




root.geometry("400x600")
root.config(bg = bcg)

entp = tk.StringVar(root, value='1')
entb = tk.StringVar(root, value='0')


map_frame = tk.Frame(root)
map_scroll = tk.Scrollbar(map_frame,bg = blu, orient=tk.VERTICAL)
map_box = tk.Listbox(map_frame,height=12 ,width=40,yscrollcommand=map_scroll.set)
map_filter = tk.Entry(map_frame,textvariable=m_filter,width=43)
map_box.config(bg = men)
map_filter.config(bg = blu)



maps.sort()

botmodes = [
    "FollowPath",
    "Swarm",
    "EggGrab"
]

inputdata = {
    "mode": "-tournament ", #lub "-gamelevel "
    "level": "",
    "playersq": "1",
    "botsq": "0",
    "botsmode": "FollowPath"
}


def single():
    global maps
    maps = maps_single
    update(maps)
    inputdata["mode"] = "-gamelevel "
    b_single.config(state='disable')
    b_episode.config(state='normal')


def episode():
    global maps
    maps = maps_episode
    update(maps)
    inputdata["mode"] = "-tournament "
    b_episode.config(state='disable')
    b_single.config(state='normal')


def update(data):
    map_box.delete(0, tk.END)
    for i in data:
        map_box.insert(tk.END, i)


def check(e):
    typed = map_filter.get()

    if typed == '':
        data = maps
    else:
        data = []
        for item in maps:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def getmap():
    inputdata["level"] = map_box.get(tk.ANCHOR)

def getlabelb(selection):
    global inputdata
    inputdata["botsmode"] = selection

def runserver():
    getmap()
    killallservers()
    global inputdata
    global ent
    if(inputdata["level"] != "choose map you wanna play"):
        inputdata["playersq"] = entp.get()
        inputdata["botsq"] = entb.get()
        cmnd=startserver1+inputdata["mode"]+inputdata["level"]+minplayer+inputdata["playersq"]+maxplayer+inputdata["playersq"]+startserver2+inputdata["botsq"]+startserver3+inputdata["botsmode"]
        #print(cmnd)
        os.system(cmnd)
        run.config(state= 'disable')

def killallservers():
    os.system(killall1)
    os.system(killall2)
    run.config(state='normal')


hi_label = tk.Label(root, text='Choose mode and map:',bg = bcg)
hi_label.pack(pady=15)

# Button Frame --> episode + single

button_frame = tk.Frame(root)
for i in all_maps[:]:
        map_box.insert(tk.END,i)
b_episode = tk.Button(button_frame, text="EPISODE",command=episode, bg="#E376AD")
b_single = tk.Button(button_frame, text="SINGLE",command=single, bg="#E376AD")
b_episode.pack(side=tk.LEFT)
b_single.pack(side=tk.RIGHT)
button_frame.pack()

# Map Frame --> listbox + scrollbar

map_scroll.config(command=map_box.yview)
map_filter.pack()
map_scroll.pack(side=tk.RIGHT,fill=tk.Y)
map_frame.pack(pady=5)
map_box.pack()




clickedb = tk.StringVar()
clickedb.set(botmodes[0])

tk.Label(root, text="Enter number of players(1-60)",bg = bcg).pack()
plq = tk.Entry(root,textvariable=entp, width=3,bg = blu).pack()

tk.Label(root, text="Enter number of bots",bg = bcg).pack()
botq = tk.Entry(root,textvariable=entb, width=3,bg = blu).pack()

tk.Label(root, text="Choose bots AI mode",bg = bcg).pack()
dropbotmode = tk.OptionMenu(root, clickedb, *botmodes,command=getlabelb)
dropbotmode.config(bg = men)
dropbotmode.pack()


run = tk.Button(root, text="Run Server", command=runserver, bg="#E376AD")
run.pack()
kill = tk.Button(root, text="Kill all servers!",command=killallservers, bg="#D63C5A")
kill.pack()
tk.Label(root, text=ip1).pack()
if(ip2 != "None"):
    tk.Label(root, text="Ip jeśli jesteś na switchu:").pack()
    tk.Label(root, text=ip2).pack()


update(maps)
map_filter.bind("<KeyRelease>",check)


root.mainloop()
