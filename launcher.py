#RealistikDash here, just be careful and wear eye protection while looking at this
from tkinter import *
from tkinter import ttk, messagebox
import minecraft_launcher_lib as MCLib
import subprocess
import ctypes
import os
import os.path
from os import path #not sure if necessary
import json
from natsort import natsorted #for version arrangement
import hashlib # for nonpremuim uuid making
import requests
from threading import Thread
import platform #for os compatibillity

Art = """ _____       __  __       __  __  _____ 
 |  __ \     |  \/  |     |  \/  |/ ____|
 | |__) |   _| \  / |_   _| \  / | |     
 |  ___/ | | | |\/| | | | | |\/| | |     
 | |   | |_| | |  | | |_| | |  | | |____ 
 |_|    \__, |_|  |_|\__, |_|  |_|\_____|
         __/ |        __/ |              
        |___/        |___/   by RealistikDash
"""
print(Art)

class JsonFile:
    @classmethod
    def SaveDict(self, Dict, File):
        """Saves a dict as a file"""
        with open(File, 'w') as json_file:
            json.dump(Dict, json_file, indent=4)

    @classmethod
    def GetDict(self, file):
        """Returns a dict from file name"""
        if not path.exists(file):
            return {}
        else:
            with open(file) as f:
                data = json.load(f)
            return data

class Config:
    #Why a class? I dont know
    Config = {} # this us loaded later on

    Version = "0.1.7MC"
    MinecraftDir = ""

    BG_Colour = '#2F3136'
    FG_Colour = "#2c3e50"

    HasInternet = True

class Data:
    Versions = { #currently not being used. for later purposes
        "1.14.4" : "http://dl.ussr.pl/example.zip"
    }

class Path:
    #class to store file paths, made for easy and quick changes
    Logo_Small = "img\\pymymc_logo_small.png"
    Logo_Icon = "img\\pymymc_ico.ico"

def MessageBox(title, content):
    """Creates a message box"""
    Update()
    #MsgThread = Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, content, title, style,))
    #MsgThread.start() #non blocking?
    messagebox.showinfo(title, content) #tkinter multiplatform messagebox rather than the windows one

def ErrorBox(title, content):
    """Creates an error dialogue box"""
    messagebox.showerror(title, content)

def WarningBox(title, content):
    """Creater a warning dialogue box"""
    messagebox.showwarning(title, content)

def ConfigWindowFunc():
    """Creates an advanced config window"""
    #i know this is not supposed to be how you do it but "it just works"
    Update()
    def SaveConfig():
        """This is the first time i use a def in a def""" #and im bad at making them
        Update()
        MCPath_Str = MCPath_StringVar.get()
        DRAM_Str = DRAM_StringVar.get()
        ForgetMe_Int = int(RememberMe_Var.get())

        NotFailedDRAMCheck = True

        try:
            DRAM_Str = int(DRAM_Str)
            if DRAM_Str <= 0:
                NotFailedDRAMCheck = False
        except Exception:
            NotFailedDRAMCheck = False #nicest way i know of doing this

        if NotFailedDRAMCheck:
            if ForgetMe_Int == 1:
                Config.Config["Email"] = ""
                Config.Config["UUID"] = ""
                Config.Config["AccessToken"] = ""
                Config.Config["Username"] = ""
            Config.Config["JVMRAM"] = DRAM_Str
            if MCPath_Str[-1] != "\\":
                MCPath_Str = MCPath_Str + "\\"
            if Premium_Var.get() == 1:
                Config.Config["Premium"] = True
            if Premium_Var.get() == 0:
                Config.Config["Premium"] = False
            Config.Config["MinecraftDir"] = MCPath_Str
            JsonFile.SaveDict(Config.Config, "config.json")
            ConfigLoad() #runs config update
            ConfigWindow.destroy()
        
        
        else:
            ErrorBox("PyMyMC Error!", "The RAM value has to be an integer (full number) over 0.")

    #Initial window settings
    ConfigWindow = Toplevel(MainWindow)
    ConfigWindow.configure(background=Config.BG_Colour) # sets bg colour
    ConfigWindow.title("PyMyMC Config") # sets window title
    ConfigWindow.iconbitmap(Path.Logo_Icon) # sets window icon
    ConfigWindow.resizable(False, False) #makes the window not resizable

    #WarningLabel
    Warning_Label = Label(ConfigWindow, text="Warning! These options are for advanced users only!", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Warning2_Label = Label(ConfigWindow, text="Proceed with caution!", bg = Config.BG_Colour, fg = "yellow", font = "none 12 bold")
    Warning_Label.grid(row=0, column=0, sticky=W)
    Warning2_Label.grid(row=1, column=0, sticky=W)

    #MC Path Label
    MCPath_Label = Label(ConfigWindow, text="Minecraft Path:", bg = Config.BG_Colour, fg = "white", font = "none 11")
    MCPath_Label.grid(row=2, column=0, sticky=W)

    #MC Path Entry
    MCPath_StringVar = StringVar()
    MCPath_Entry = ttk.Entry(ConfigWindow, width=40, textvariable=MCPath_StringVar)
    MCPath_StringVar.set(Config.Config["MinecraftDir"])
    MCPath_Entry.grid(row=3, column=0, sticky=W)

    #Dedicated RAM Label
    DRAM_Label = Label(ConfigWindow, text="JVM Dedicated RAM:", bg = Config.BG_Colour, fg = "white", font = "none 11")
    DRAM_Label.grid(row=4,column=0,sticky=W) 

    #Dedicated RAM Entry
    DRAM_StringVar = StringVar()
    DRAM_Entry = ttk.Entry(ConfigWindow, width=10, textvariable=DRAM_StringVar)
    DRAM_StringVar.set(Config.Config["JVMRAM"])
    DRAM_Entry.grid(row=5, column=0, sticky=W)

    GB_Label = Label(ConfigWindow, text="GB", bg = Config.BG_Colour, fg = "white", font = "none 9")
    GB_Label.grid(row=5, column=0, sticky=E)

    #ForgetMe RADIO
    RememberMe_Var = IntVar() #value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(ConfigWindow, text="Forget Me", variable=RememberMe_Var)
    RememberMe_Checkbox.grid(row=6, column=0, sticky=W)

    #Premium RADIO
    Premium_Var = IntVar() #value whether its ticked is stored here
    if Config.Config["Premium"]:
        Premium_Var.set(1) #sets to whats enabled
    Premium_Checkbox = ttk.Checkbutton(ConfigWindow, text="Use Premium Minecraft Accounts", variable=Premium_Var)
    Premium_Checkbox.grid(row=7, column=0, sticky=W)
    
    #Apply Button
    Apply_Button = ttk.Button(ConfigWindow, text="Apply", width=10, command = SaveConfig)
    Apply_Button.grid(row=8, column=0, sticky=W)

    #Cancel Button
    Cancel_Button = ttk.Button(ConfigWindow, text="Cancel", width=10, command = ConfigWindow.destroy)
    Cancel_Button.grid(row=8, column=0, sticky=E)

def Install(PlayAfter = False):
    """Installs minecraft"""
    #Version = "1.14.4" #later change it into a gui list # i did
    Update()
    Version = ListVariable.get()

    MinecraftFound = path.exists(Config.MinecraftDir+f"versions\\{Version}\\")
    if MinecraftFound:
        MessageBox("PyMyMC Info!", "This version is already installed! Press play to play it!")

    elif not Config.HasInternet:
        ErrorBox("PyMyMC Error!", "An internet connection is required for this action!")

    else:
        MessageBox("PyMyMC Info!", "Downloading started! If you pressed play to download, the program will freeze.")
        callback = {
            "setStatus": SetStatusHandler,
            "setProgress" : SetProgressHandler,
            "setMax": SetMaxHandler,
        }
        #MCLib.install.install_minecraft_version(Version, Config.MinecraftDir, callback=callback)
        DlThread = Thread(target=MCLib.install.install_minecraft_version, args=(Version, Config.MinecraftDir,), kwargs={"callback" : callback})
        DlThread.start()
        if PlayAfter:
            DlThread.join()
            Play()

def Play():
    """Function that is done when the play button is pressed"""
    #Note 25/12/19 | Deal with sessions expiring
    
    Update()
    Email = Username_Entry.get()
    Password = Password_Entry.get()
    Version = ListVariable.get()
    RememberMe = False
    if RememberMe_Var.get() == 1:
        RememberMe = True

    if not Config.Config["Premium"] or not Config.HasInternet:
        #NonPremium code
        if Email == "":
            WarningBox("PyMyMC Error!", "Username cannot be empty!")
        else:
            if Config.Config["Premium"]:
                #code for getting a username rather than email
                TempName = Email.split("@")
                Email = TempName[0]
            options = {
                "username" : Email,
                "uuid" : str(hashlib.md5(str.encode(Email)).digest()),
                "token" : "",
                "launcherName": "PyMyMC",
                "gameDirectory": Config.MinecraftDir,
                "jvmArguments" : [f"-Xmx{Config.Config['JVMRAM']}G"]
            }

            if RememberMe:
                Config.Config["Email"] = Email
                JsonFile.SaveDict(Config.Config, "config.json")

            Config.Config["LastSelected"] = Version
            JsonFile.SaveDict(Config.Config, "config.json") #last version saving
            
            Command = MCLib.command.get_minecraft_command(Version, Config.MinecraftDir, options)
            MainWindow.destroy()
            
            subprocess.call(Command)
            MessageBox("PyMyMC", "Thank you for using PyMyMC!")

    if Config.Config["Premium"] and Config.HasInternet:
        if Email == "":
            ErrorBox("PyMyMC Error!", "Username cannot be empty!")
        elif Password == "" and Email != Config.Config["Email"]:
            ErrorBox("PyMyMC Error!", "Password cannot be empty!")
        else:
            if Email != Config.Config["Email"] or Config.Config["UUID"] == "" or Config.Config["AccessToken"] == "":
                AccountInfo = MCLib.account.login_user(Email, Password) # so it doesnt do it with the __useuuid__PyMyMC__ password
                UsingPassword = True
            else:
                AccountInfo = {} #so i dont have to make 2 different checks for errors
                UsingPassword = False

            if "error" in list(AccountInfo.keys()):
                ErrorBox("PyMyMC Error!", AccountInfo["errorMessage"])
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

                if MinecraftFound:
                    options = {
                        "username" : Username,
                        "uuid" : Uuid,
                        "token" : AccessToken,

                        "launcherName": "PyMyMC",
                        "gameDirectory": Config.MinecraftDir,
                        "jvmArguments" : [f"-Xmx{Config.Config['JVMRAM']}G"]
                    }
                    Command = MCLib.command.get_minecraft_command(Version, Config.MinecraftDir, options)
                    MainWindow.destroy()
                    if RememberMe:
                        Config.Config["Email"] = Email
                        Config.Config["AccessToken"] = AccessToken
                        Config.Config["UUID"] = Uuid
                        Config.Config["Username"] = Username
                        JsonFile.SaveDict(Config.Config, "config.json") #saves credentials to config.json
                    Config.Config["LastSelected"] = Version
                    JsonFile.SaveDict(Config.Config, "config.json") #last version saving
                    subprocess.call(Command)
                    MessageBox("PyMyMC", "Thank you for using PyMyMC!")
                else:
                    Install(True)

def ConfigLoad():
    """Function to load/make new config"""
    ExampleConfig = {
        "IsExample" : False,
        "MinecraftDir" : os.getenv('APPDATA') + "\\.minecraft\\",
        "Email" : "",
        "UUID" : "", #remember kids, never store passwords
        "AccessToken" : "",
        "JVMRAM" : 2, #in GB
        "Premium" : True,
        "LastSelected" : "1.15.1"
    }

    JSONConfig = JsonFile.GetDict("config.json")
    if JSONConfig == {}:
        JSONConfig = ExampleConfig
        JsonFile.SaveDict(JSONConfig, "config.json")

    if JSONConfig["IsExample"] == True:
        Config.Config = ExampleConfig
    else:
        Config.Config = JSONConfig

    Config.MinecraftDir = Config.Config["MinecraftDir"]  

    #Making older configs compatible with newer ones
    if "JVMRAM" not in list(Config.Config.keys()):
        #for reuse of older configs
        Config.Config["JVMRAM"] = 2
        JsonFile.SaveDict(Config.Config, "config.json")
    
    if "Premium" not in list(Config.Config.keys()):
        Config.Config["Premium"] = True
        JsonFile.SaveDict(Config.Config, "config.json")

    if "LastSelected" not in list(Config.Config.keys()):
        Config.Config["LastSelected"] = "1.15.1"
        JsonFile.SaveDict(Config.Config, "config.json")

def InternetStatus():
    """Checks for a working internet connection"""
    TestURL = "http://google.co.uk/"
    try:
        requests.get(TestURL, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def ExitHandler():
    """Function ran on the closing of the tk mainwindow"""
    MainWindow.destroy()
    exit()

def SetStatusHandler(status):
    Download_Progress["value"] = 0
    print(status)

def SetProgressHandler(status):
    Download_Progress["value"] = int(status)
    

def SetMaxHandler(status):
    Download_Progress["maximum"] = int(status)

def Update():
    """Function ran on every part of the code to make sure everything is right"""
    Config.HasInternet = InternetStatus()

#Initialising
ConfigLoad()
MainWindow = Tk()
if __name__ == '__main__':
    Update()
    #Styles
    s = ttk.Style()
    s.configure('TButton', background=Config.FG_Colour, fieldbackground=Config.FG_Colour)
    s.configure('TCheckbutton', background=Config.BG_Colour, foreground="white")
    s.configure('TEntry', fieldbackground=Config.FG_Colour)

    MainWindow.configure(background=Config.BG_Colour) # sets bg colour
    MainWindow.title("PyMyMC") # sets window title
    MainWindow.iconbitmap(Path.Logo_Icon) # sets window icon
    MainWindow.resizable(False, False) #makes the window not resizable
    MainWindow.protocol("WM_DELETE_WINDOW", ExitHandler) #runs the function when the user presses the X button

    #Logo Image
    PyMyMC_Logo = PhotoImage(file=Path.Logo_Small)
    PyMyMC_Logo_Label = Label(MainWindow, image=PyMyMC_Logo)
    PyMyMC_Logo_Label['bg'] = PyMyMC_Logo_Label.master['bg']
    PyMyMC_Logo_Label.grid(row=0, column=0) 

    #Info Label
    PInfo_Label = Label(MainWindow, text=f"PyMyMC {Config.Version}", bg=Config.BG_Colour, fg = 'white', font = "Arial 15 bold")
    PInfo2_Label = Label(MainWindow, text="Made by RealistikDash", bg=Config.BG_Colour, fg = 'white', font = "none 13")
    PInfo_Label.grid(row=2, column=0, sticky=W)
    PInfo2_Label.grid(row=3, column=0, sticky=W)

    #Username Label
    Username_Label = Label(MainWindow, text="Email:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    if not Config.Config["Premium"]:
        Username_Label["text"] = "Username:"
    Username_Label.grid(row=5, column=0, sticky=W)

    #Username Entry
    US_EntryText = StringVar() #
    Username_Entry = ttk.Entry(MainWindow, width=40, textvariable=US_EntryText)
    US_EntryText.set(Config.Config["Email"]) #inserts config email here
    Username_Entry.grid(row=6, column = 0, sticky=W)

    #Password Label
    Password_Label = Label(MainWindow, text="Password:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Password_Label.grid(row=7, column=0, sticky=W)

    #Password Entry
    Password_Entry = ttk.Entry(MainWindow, width=40, show="*")
    Password_Entry.grid(row=8, column = 0, sticky=W)

    #Play Button
    Play_Button = ttk.Button(MainWindow, text="Play!", width=10, command = Play)
    Play_Button.grid(row = 11, column=0, sticky = W)

    #Install Button
    Install_Button = ttk.Button(MainWindow, text="Download!", width=10, command = Install)
    Install_Button.grid(row = 11, column=0, sticky = E)

    #Version Label
    Password_Label = Label(MainWindow, text="Version:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Password_Label.grid(row=9, column=0, sticky=W)

    #Version list
    try:
        #So the launcher still works if internet not here
        MCVerList = MCLib.utils.get_version_list()
    except Exception:
        MCVerList = []
    McVers = []

    # Code for searching for existing versions
    if path.exists(Config.MinecraftDir+"versions\\"):
        VersionList = os.listdir(Config.MinecraftDir+"versions\\")
        for Realistik in VersionList:
            McVers.append(Realistik)

    for RealistikDash in MCVerList:
        RealistikDash = RealistikDash["id"]
        if "w" not in RealistikDash and "pre" not in RealistikDash and "Pre-Release" not in RealistikDash and "Pre1" not in RealistikDash and RealistikDash not in McVers: #gets rid of snapshots and pre-releases
            McVers.append(RealistikDash)
    McVers = natsorted(McVers)
    McVers.insert(0, Config.Config["LastSelected"]) #using a bug in ttk to our advantage

    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *McVers)
    Ver_List.grid(row=10, column=0, sticky=W)

    #Config Button
    Config_Button = ttk.Button(MainWindow, text="Config",  width=10, command = ConfigWindowFunc)
    Config_Button.grid(row = 11, column=0)

    #Remember Me Checkbox
    RememberMe_Var = IntVar() #value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(MainWindow, text="Remember me", variable=RememberMe_Var)
    RememberMe_Checkbox.grid(row=10, column=0, sticky=E)

    #Download Progress Bar
    Download_Progress = ttk.Progressbar(MainWindow, length=245)
    Download_Progress.grid(row=12, column=0)

    MainWindow.mainloop()