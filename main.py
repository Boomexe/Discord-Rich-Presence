from pypresence import Presence
import tkinter as tk
from tkinter import messagebox
import json
import os
from sys import exit

import pystray
from PIL import Image, ImageTk

cwd = os.getcwd()
assetsDir = os.path.join(cwd,'assets')
discordIconDir = os.path.join(assetsDir,'discord_icon.ico')
discordPngDir = os.path.join(assetsDir,'discord_icon.png')
settingsDir = os.path.join(cwd,'settings','settings.json')

def showNotif(Title,Text): 
    messagebox.showinfo(Title, Text)

def showError(Title,Text):
    messagebox.showerror(Title,Text)


def loadSettings():
    global settings

    with open(settingsDir,'r') as data:
        settings = json.load(data)

def saveSettings():
    with open(settingsDir,'w') as data:

       settings['application_id'] = applicationIdEntry.get()
       settings['large_image'] = largeImageEntry.get()
       settings['details'] = detailsEntry.get()
       settings['state'] = stateEntry.get()
       
       json.dump(settings,data)

loadSettings()

# Presence Variables
discordAppId = settings['application_id']
largeImage = settings['large_image']
details = settings['details']
state = settings['state']

def connectToDiscord():
    global rpc
    try:
        rpc = Presence(discordAppId)
        rpc.connect()
    except:
        print('Could not connect to Discord! Make sure you have Discord open.')
        showError('Error','Could not connect to Discord! Make sure you have Discord open.')

connectToDiscord()

def updateDiscordPresence():
    saveSettings()
    try:
        rpc.update(
            details = details,
            state = state,
            large_image = largeImage
        )
        showNotif('Notification','Successfully updated Discord presence.')
        print('Successfully updated Discord presence.')

    except:
        connectToDiscord()
        print('Could not update Discord presence!')
        showError('Error','Could not update Discord presence!')


window = tk.Tk()
window.title('Custom Discord Rich Presence')
window.iconbitmap(discordIconDir)
window.geometry('800x800')

def quitPrompt(Title,Text):
    quitPrompt = messagebox.askokcancel(Title,Text)
    if quitPrompt == True:
        window.destroy()
        exit()

def quitNoPrompt(icon):
    icon.stop()
    window.destroy()
    exit()

def showWindow(icon):
   icon.stop()
   window.after(0, window.deiconify())

def hideWindow():
   window.withdraw()
   image = Image.open(discordPngDir)
   menu  = (pystray.MenuItem('Show', showWindow), pystray.MenuItem('Quit', quitNoPrompt))
   icon  = pystray.Icon("name", image, "Discord Rich Presence", menu)
   icon.run()

titleLabel = tk.Label(
    text   = "CUSTOM DISCORD RICH PRESENCE",
    font   = ('Times New Roman',30),
    height = 3
)

# Application ID Widgets
applicationIdLabel = tk.Label(
    text = 'Discord Application ID:',
    font = ('Times New Roman',12)
)

applicationIdEntry = tk.Entry(
    width   = 25,
    justify = tk.CENTER
)

applicationIdEntry.insert(0,discordAppId)

# Large image Widgets
largeImageLabel = tk.Label(
    text = 'Image (set to name of asset):',
    font = ('Times New Roman',12)
)

largeImageEntry = tk.Entry(
    width   = 25,
    justify = tk.CENTER
)

largeImageEntry.insert(0,largeImage)

# Details Widgets
detailsLabel = tk.Label(
    text = 'Details:',
    font = ('Times New Roman',12)
)

detailsEntry = tk.Entry(
    width   = 45,
    justify = tk.CENTER
)

detailsEntry.insert(0,details)

# State Widgets
stateLabel = tk.Label(
    text = 'State:',
    font = ('Times New Roman',12)
)
stateEntry = tk.Entry(
    width   = 45,
    justify = tk.CENTER
)

stateEntry.insert(0,state)

startButton = tk.Button(
    text    = 'Start/Update',
    font = ('Times New Roman',12),
    command = lambda: updateDiscordPresence()
)

minimizeToTray = tk.Button(
    text    = 'Minimize to Tray',
    font = ('Times New Roman',12),
    command = lambda: hideWindow()
)

quitButton = tk.Button(
    text    = 'Quit',
    font = ('Times New Roman',12),
    command = lambda: quitPrompt('Quit?','Are you sure you want to quit? Your Discord activity status will disappear')
)

titleLabel.pack()

applicationIdLabel.pack()
applicationIdEntry.pack()

largeImageLabel.pack()
largeImageEntry.pack()

detailsLabel.pack()
detailsEntry.pack()

stateLabel.pack()
stateEntry.pack()

startButton.pack()
minimizeToTray.pack()
quitButton.pack()

window.protocol("WM_DELETE_WINDOW", hideWindow)#window.iconify)

window.mainloop()