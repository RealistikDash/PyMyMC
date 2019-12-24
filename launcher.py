from tkinter import *
import minecraft_launcher_lib as MCLib
import subprocess
import ctypes
import os
import os.path
from os import path #not sure if necessary
import json

class JsonFile:
    @classmethod
    def SaveDict(self, Dict, File):
        """Saves a dict as a file"""
        with open(File, 'w') as json_file:
            json.dump(Dict, json_file, indent=4)

    @classmethod
    def GetDict(self, file):
        """Returns a dict from file name"""
        with open(file) as f:
            data = json.load(f)
        return data

class Config:
    #Why a class? I dont know
    Config = {} # this us loaded later on

    Version = "0.1.1"
    MinecraftDir = ""

    BG_Colour = '#424242'

class Data:
    Versions = { #currently not being used. for later purposes
        "1.14.4" : "http://dl.ussr.pl/example.zip"
    }

def MessageBox(title, content, style = 0):
    """Creates a Windows message box"""
    #title = title.encode('utf-8') #apparently not needed
    #content = content.encode('utf-8') #apparently not needed
    ctypes.windll.user32.MessageBoxW(0, content, title, style)

    ##  Styles:
    ##  0 : OK
    ##  1 : OK | Cancel
    ##  2 : Abort | Retry | Ignore
    ##  3 : Yes | No | Cancel
    ##  4 : Yes | No
    ##  5 : Retry | No 
    ##  6 : Cancel | Try Again | Continue

def Install(PlayAfter = False):
    """Installs minecraft"""
    #Version = "1.14.4" #later change it into a gui list
    Version = ListVariable.get()

    MinecraftFound = path.exists(Config.MinecraftDir+f"versions\\{Version}\\")
    if MinecraftFound:
        MessageBox("PyMyMC Info!", "This version is already installed! Press play to play it!")

    else:
        MessageBox("PyMyMC Info!", "Downloading started! The program may be frozen for a few minutes. Don't touch it while it's frozen.")
        MCLib.install.install_minecraft_version(Version, Config.MinecraftDir, callback=None)
        if PlayAfter:
            Play()
        else:
            MessageBox("PyMyMC Info!", "Downloading Minecraft finished! You can now play!")

def Play():
    """Function that is done when the play button is pressed"""
    Email = Username_Entry.get()
    Password = Password_Entry.get()
    Version = ListVariable.get()

    #print(Username)
    #print(Config.MinecraftDir)

    if Email == "":
        MessageBox("PyMyMC Error!", "Username cannot be empty!")
    elif Password == "" and Email != Config.Config["Email"]:
        MessageBox("PyMyMC Error!", "Password cannot be empty!")
    else:
        if Email != Config.Config["Email"] or Config.Config["UUID"] == "" or Config.Config["AccessToken"] == "":
            AccountInfo = MCLib.account.login_user(Email, Password) # so it doesnt do it with the __useuuid__PyMyMC__ password
            UsingPassword = True
        else:
            AccountInfo = {} #so i dont have to make 2 different checks for errors
            UsingPassword = False

        if "error" in list(AccountInfo.keys()):
            MessageBox("PyMyMC Error!", AccountInfo["errorMessage"])
        else:
            if UsingPassword:
                AccessToken = AccountInfo["accessToken"]
                Username = AccountInfo["selectedProfile"]["name"]
                Uuid = AccountInfo["selectedProfile"]["id"]
            else:
                #grabs from the config
                AccessToken = Config.Config["AccessToken"]
                Username = Config.Config["Username"]
                Uuid = Config.Config["UUID"]


            #RealistikDash was here
            MinecraftFound = path.exists(Config.MinecraftDir+f"versions\\{Version}\\")

            #debugging
            print(f"Access Token: {AccessToken}")
            print(f"UUID: {Uuid}")

            if MinecraftFound:
                options = {
                    "username" : Username,
                    "uuid" : Uuid,
                    "token" : AccessToken,

                    "launcherName": "PyMyMC",
                    "gameDirectory": Config.MinecraftDir
                }
                Command = MCLib.command.get_minecraft_command(Version, Config.MinecraftDir, options)
                MainWindow.destroy()
                subprocess.call(Command)
                MessageBox("PyMyMC", "Thank you for using PyMyMC!")
            else:
                Install(True)

def ConfigLoad():
    """Function to load/make new config"""
    ExampleConfig = {
        "IsExample" : False,
        "MinecraftDir" : os.getcwd() + "\\.minecraft\\",
        "Email" : "",
        "UUID" : "", #remember kids, never store passwords
        "AccessToken" : ""
    }

    JSONConfig = JsonFile.GetDict("config.json")

    if JSONConfig["IsExample"] == True:
        Config.Config = ExampleConfig
    else:
        Config.Config = JSONConfig

    Config.MinecraftDir = Config.Config["MinecraftDir"]  

ConfigLoad()
MainWindow = Tk()
MainWindow.configure(background=Config.BG_Colour) # sets bg colour
MainWindow.title("PyMyMC") # sets window title
MainWindow.iconbitmap("img\\pymymc_ico.ico") # sets window icon
MainWindow.resizable(False, False) #makes the window not resizable

#Logo Image
PyMyMC_Logo = PhotoImage(file="img\\pymymc_logo_small.png")
PyMyMc_Logo_Label = Label(MainWindow, image=PyMyMC_Logo)
PyMyMc_Logo_Label['bg'] = PyMyMc_Logo_Label.master['bg']
PyMyMc_Logo_Label.grid(row=0, column=0) 

#Info Label
PInfo_Label = Label(MainWindow, text=f"PyMyMC {Config.Version}", bg=Config.BG_Colour, fg = 'white', font = "none 15 bold")
PInfo2_Label = Label(MainWindow, text="Made by RealistikDash", bg=Config.BG_Colour, fg = 'white', font = "none 13")
PInfo_Label.grid(row=2, column=0, sticky=W)
PInfo2_Label.grid(row=3, column=0, sticky=W)

#Username Label
Username_Label = Label(MainWindow, text="Email:", bg = Config.BG_Colour, fg = "white", font = "none 12")
Username_Label.grid(row=5, column=0, sticky=W)

#Username Entry
US_EntryText = StringVar() #
Username_Entry = Entry(MainWindow, width=40, bg = "grey", fg="white", textvariable=US_EntryText)
US_EntryText.set(Config.Config["Email"]) #inserts config email here
Username_Entry.grid(row=6, column = 0, sticky=W)

#Password Label
Password_Label = Label(MainWindow, text="Password:", bg = Config.BG_Colour, fg = "white", font = "none 12")
Password_Label.grid(row=7, column=0, sticky=W)

#Password Entry
Password_Entry = Entry(MainWindow, width=40, bg = "grey", fg="white", show="*")
Password_Entry.grid(row=8, column = 0, sticky=W)

#Play Button
Play_Button = Button(MainWindow, text="Play!", bg = "grey", fg = "white", width=10, command = Play)
Play_Button.grid(row = 11, column=0, sticky = W)

#Install Button
Install_Button = Button(MainWindow, text="Download!", bg = "grey", fg = "white", width=10, command = Install)
Install_Button.grid(row = 11, column=0, sticky = E)

#Version Label
Password_Label = Label(MainWindow, text="Version:", bg = Config.BG_Colour, fg = "white", font = "none 12")
Password_Label.grid(row=9, column=0, sticky=W)

#Version list
MCVerList = MCLib.utils.get_version_list()
McVers = []

for RealistikDash in MCVerList:
    RealistikDash = RealistikDash["id"]
    if "w" not in RealistikDash and "pre" not in RealistikDash and "Pre-Release" not in RealistikDash and "Pre1" not in RealistikDash: #gets rid of snapshots and pre-releases
        McVers.append(RealistikDash)

ListVariable = StringVar(MainWindow)
ListVariable.set(McVers[0])
Ver_List = OptionMenu(MainWindow, ListVariable, *McVers)
Ver_List.grid(row=10, column=0, sticky=W)

#Remember Me Checkbox
RememberMe_Checkbox = Checkbutton(MainWindow, text="Remember me", bg=Config.BG_Colour, fg = "white")
RememberMe_Checkbox.grid(row=10, column=0, sticky=E)

MainWindow.mainloop()