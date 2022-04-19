from pypresence import Presence
from time import sleep
import tkinter as tk
from tkinter import messagebox
import json
from os import getcwd, path
from os.path import join
from sys import exit


cwd = getcwd()
assetsDir = path.join(cwd,'assets')
discordIconDir = path,join(assetsDir,'discordicon.ico')
settingDir = path.join(cwd,'settings.json')

success = False

window = tk.Tk()
window.title('Custom Discord Rich Presence')
window.iconbitmap('discordicon.ico')
window.geometry('800x800')

def loadSettings():
    global settings

    with open(settingDir,'r') as data:
        settings = json.load(data)

def saveSettings():
    with open(settingDir,'w') as data:
        json.dump(settings,data)

loadSettings()

def showNotif(Title,Text): 
    messagebox.showinfo(Title, Text)

def showError(Title,Text):
    messagebox.showerror(Title,Text)


def quit(Title,Text):
    quitPrompt = messagebox.askokcancel(Title,Text)
    if quitPrompt == True:
        exit()

applicationId = settings['application_id']
largeImage = settings['large_image']
details = settings['details']
state = settings['state']

def checkBlank():
    global applicationId
    if applicationId == '':
        applicationId = input('Discord application id not found! Please enter one here\n>>> ')
        if applicationId == '':
            checkBlank()

print('Started Discord Presence')

def startPresence():
    global rpc
    global largeImage
    global details
    global state

    saveSettings()

    try:
        rpc = Presence(applicationId)
        rpc.connect()

        showNotif('Notification','Rich Presences Updated.')

        try:
            rpc.update(
                details = details,
                state =  state,
                large_image = largeImage
            )
        
        except:
            showError('ERROR','Could not update Discord Rich Presence! Make sure you have your Discord launched.')
    
    except:
        showError('ERROR','Could not connect to Discord! Make sure you have your Discord launched.')

titleLabel = tk.Label(
    text="CUSTOM DISCORD RICH PRESENCE",
    font=('Times New Roman',30),
    height=3
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

applicationIdEntry.insert(0,applicationId)

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
    text = 'Details:',
    font = ('Times New Roman',12)
)
stateEntry = tk.Entry(
    width   = 45,
    justify = tk.CENTER
)

stateEntry.insert(0,state)

startButton = tk.Button(
    text    = 'START/UPDATE',
    font = ('Times New Roman',12),
    command = lambda: startPresence()
)

quitButton = tk.Button(
    text    = 'QUIT',
    font = ('Times New Roman',12),
    command = lambda: quit('Quit?','Are you sure you want to quit? Your Discord Activity Status will disappear')
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
quitButton.pack()

window.protocol("WM_DELETE_WINDOW", window.iconify)

window.mainloop()