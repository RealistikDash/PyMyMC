#RealistikDash here, just be careful and wear eye protection while looking at this
from tkinter import *
from tkinter import ttk, messagebox
import minecraft_launcher_lib as MCLib
import subprocess
import os
import os.path
from os import path #not sure if necessary
import json
from natsort import natsorted #for version arrangement
import hashlib # for nonpremuim uuid making
import requests
from threading import Thread
import platform #for os compatibillity
import pathlib #for getting home folder
from colorama import init, Fore #for coloured text within the console
from datetime import datetime #for getting and formatting current time
import random
from pypresence import Presence
from ttkthemes import ThemedTk #for custom themes! i like

Art = """ _____       __  __       __  __  _____ 
 |  __ \     |  \/  |     |  \/  |/ ____|
 | |__) |   _| \  / |_   _| \  / | |     
 |  ___/ | | | |\/| | | | | |\/| | |     
 | |   | |_| | |  | | |_| | |  | | |____ 
 |_|    \__, |_|  |_|\__, |_|  |_|\_____|
         __/ |        __/ |              
        |___/        |___/   by RealistikDash
"""
init() #initialises colorama
print(random.choice([Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.WHITE, Fore.CYAN, Fore.GREEN]) + Art + Fore.RESET)
System = platform.system() #prevents system func from always being called

class Config:
    #Why a class? I dont know
    Config = {} # this is loaded later on

    Version = "0.1.7MC"
    MinecraftDir = ""

    BG_Colour = '#2F3136'
    FG_Colour = "#2c3e50"
    Theme = "equilux"

    HasInternet = True
    ShowHistorical = False

    #Discord Rich Presence Settings
    RPCEnable = False
    ClientId = "673338815301287966"
    LargeImage = "pymymc_logo"
    ConfigImage = "config"
    RootImage = "main"
    VanillaImage = "vanilla"
    ModdedImage = "modded"

    #More advanced options
    # If set to true, the System ver will be set to "Linux" to help test things. That variable is used by PyMyMC
    # to check what OS the user is using (eg Windows, Linux, MacOS/Darwin)
    FakeLinux = False 
    # Leave blank for no proxy. This will route all the requests from PyMyMC (not its modules) via the provided proxy.
    # The proxy must support being invoked directly and must support JSON. The main purpose of this is to bypass any
    # blocks of the Mojang and Minecraft webste (which I need for my primary use of this lanucher). Using a slow
    # proxy can slow down this program so i recommend not using one unless completely necessary. Setting this proxy
    # incorrectly can cause the launcher to have connection problems and for now there is no check for it.
    Proxy = "" 
    if FakeLinux:
        #done in the class so the later on code isnt broken
        System = "Linux"

    #GUI properties for different systems
    ## On some systems (namely linux) widget size would be way different than on my 
    ## development environment (Windows) so this part of the code makes sure things
    ## look at least similar on most major systems.
    if System == "Windows":
        BoxWidth = 10
        EntryLen = 40
        BarLen = 245
        ListLen = 15
    else:
        BoxWidth = 7
        EntryLen = 30
        BarLen = 245
        ListLen = 8

class A:
    """Aliases"""
    #Colorama Aliases
    red = Fore.RED
    blue = Fore.BLUE
    black = Fore.BLACK
    res = Fore.RESET
    yellow = Fore.YELLOW
    green = Fore.GREEN
    magenta = Fore.MAGENTA

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

class Path:
    #class to store file paths, made for easy and quick changes
    if System == "Windows":
        Logo_Small = "img\\pymymc_logo_small.png"
        Logo_Icon = "img\\pymymc_ico.ico"
    else:
        Logo_Small = "img/pymymc_logo_small.png"
        Logo_Icon = "img/pymymc_logo_small.png"

def MessageBox(title, content):
    """Creates a message box"""
    Update()
    #MsgThread = Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, content, title, style,))
    #MsgThread.start() #non blocking?
    MsgThread = Thread(target=messagebox.showinfo, args=(title, content,))
    MsgThread.start()
    #messagebox.showinfo(title, content) #tkinter multiplatform messagebox rather than the windows one
    print(A.blue + f"[{FormatTime()}]", content + A.res)

def ErrorBox(title, content):
    """Creates an error dialogue box"""
    MsgThread = Thread(target=messagebox.showerror, args=(title, content,))
    MsgThread.start()
    #messagebox.showerror(title, content)
    print(A.red + f"[{FormatTime()}]", content + A.res)

def WarningBox(title, content):
    """Creater a warning dialogue box"""
    MsgThread = Thread(target=messagebox.showwarning, args=(title, content,))
    MsgThread.start()
    #messagebox.showwarning(title, content)
    print(A.yellow + f"[{FormatTime()}]", content + A.res)

def ConfigWindowFunc():
    """Creates an advanced config window"""
    #i know this is not supposed to be how you do it but "it just works"
    Update()

    def ConfigCloseProtocol():
        """Function ran when the config window is closed"""
        ConfigWindow.destroy()
        DefaultPresence()

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
            if System == "Windows":
                if MCPath_Str[-1] != "\\":
                    MCPath_Str = MCPath_Str + "\\"
            else:
                #other systems use / instead of \
                if MCPath_Str[-1] != "/":
                    MCPath_Str = MCPath_Str + "/"
            if Premium_Var.get() == 1:
                Config.Config["Premium"] = True
            if Premium_Var.get() == 0:
                Config.Config["Premium"] = False
            if Historical_Var.get() == 0:
                Config.Config["OnlyReleases"] = True
            if Historical_Var.get() == 1:
                Config.Config["OnlyReleases"] = False
            Config.Config["MinecraftDir"] = MCPath_Str
            JsonFile.SaveDict(Config.Config, "config.json")
            ConfigLoad() #runs config update
            ConfigWindow.destroy()
            PopulateRoot()
        
        
        else:
            ErrorBox("PyMyMC Error!", "The RAM value has to be an integer (full number) over 0.")

    #Discord Rich Presence Update
    if Config.RPCEnable:
        RPC.update(state="Configuring things...", small_image=Config.ConfigImage, large_image=Config.LargeImage)
    #Initial window settings
    ConfigWindow = Toplevel(MainWindow)
    ConfigWindow.configure(background=Config.BG_Colour) # sets bg colour
    ConfigWindow.title("PyMyMC Config") # sets window title
    ConfigWindow.protocol("WM_DELETE_WINDOW", ConfigCloseProtocol)
    if System == "Windows":
        #other systems dont use ico
        MainWindow.iconbitmap(Path.Logo_Icon) # sets window icon
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

    #Show Historical
    Historical_Var = IntVar()
    if not Config.Config["OnlyReleases"]:
        Historical_Var.set(1)
    Historical_Checkbox = ttk.Checkbutton(ConfigWindow, text="Show non-release versions", variable=Historical_Var)
    Historical_Checkbox.grid(row=8, column=0, sticky=W)
    
    #Apply Button
    Apply_Button = ttk.Button(ConfigWindow, text="Apply", width=Config.BoxWidth, command = SaveConfig)
    Apply_Button.grid(row=9, column=0, sticky=W)

    #Cancel Button
    Cancel_Button = ttk.Button(ConfigWindow, text="Cancel", width=Config.BoxWidth, command = ConfigWindow.destroy)
    Cancel_Button.grid(row=9, column=0, sticky=E)

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
    def PlayRPCUpdate(version, username, isPremium):
        """Updates the rich presence so i dont have to copy and paste the same code on premium and nonpremium"""
        #Checks if the user is playing vanilla mc or modded for RPC icon
        if Config.RPCEnable:
            IsVanilla = True
            MCVerList = MCLib.utils.get_version_list()
            VerList = []
            for thing in MCVerList:
                VerList.append(thing["id"])
            if version in VerList:
                IsVanilla = True
            else:
                IsVanilla = False
            if IsVanilla:
                SmallIcon = Config.VanillaImage
            else:
                SmallIcon = Config.ModdedImage

            #Details text
            if not isPremium:
                PrState = ", non-premuim"
            else:
                PrState = ""
            RPC.update(state=f"Playing Minecraft {version}", large_image=Config.LargeImage, small_image=SmallIcon, details=f"Playing as {username}{PrState}")


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
            PlayRPCUpdate(Version, Email, False)
            
            subprocess.call(Command)
            #MessageBox("PyMyMC", "Thank you for using PyMyMC!") #Temporarily disabled as it would create an empty tk window

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
                    PlayRPCUpdate(Version, Username, True)
                    JsonFile.SaveDict(Config.Config, "config.json") #last version saving
                    subprocess.call(Command)
                    #MessageBox("PyMyMC", "Thank you for using PyMyMC!")
                else:
                    Install(True)

def ConfigLoad():
    """Function to load/make new config"""
    if System == "Windows":
        MCDir = os.getenv('APPDATA') + "\\.minecraft\\"
    else:
        #I dont know if this will work with macs or not
        MCDir = str(pathlib.Path.home()) + "/.minecraft/"
    ExampleConfig = {
        "IsExample" : False,
        "MinecraftDir" : MCDir,
        "Email" : "",
        "UUID" : "", #remember kids, never store passwords
        "AccessToken" : "",
        "JVMRAM" : 2, #in GB
        "Premium" : True,
        "LastSelected" : "1.15.1",
        "OnlyReleases" : True,
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
    
    if "OnlyReleases" not in list(Config.Config.keys()):
        Config.Config["OnlyReleases"] = True
        JsonFile.SaveDict(Config.Config, "config.json")
        Config.ShowHistorical = False

    #Only Releases Fixes. Not cleanest way of doing it but gets the job done
    if Config.Config["OnlyReleases"]:
        Config.ShowHistorical = False
    else:
        Config.ShowHistorical = True

def InternetStatus():
    """Checks for a working internet connection"""
    TestURL = "http://minecraft.net/"
    try:
        requests.get(Config.Proxy + TestURL, timeout=5)
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

def GetReleases():
    """Returns a list of all full mc releases"""
    Releases = []
    Lista = requests.get(Config.Proxy + "https://launchermeta.mojang.com/mc/game/version_manifest.json").json() # gets ALL version info
    VersionsA = Lista["versions"]
    for key in VersionsA:
        if key["type"] == "release":
            Releases.append(key)
    return Releases

def FormatTime(format="%H:%M:%S"):
    """Formats the current time"""
    Now = datetime.now()
    return Now.strftime(format)

def DefaultPresence():
    """Sets the default presence"""
    if Config.RPCEnable:
        RPC.update(state="In the main menu.", large_image=Config.LargeImage, small_image=Config.RootImage)

def PopulateRoot():
    """Populates the fields in this function to make the window show up faster"""
    print("Populating...")
    if not Config.Config["Premium"]:
        Username_Label["text"] = "Username:"
    else:
        Username_Label["text"] = "Email"
    
    #Version list
    try:
        #So the launcher still works if internet not here
        if Config.ShowHistorical:
            MCVerList = MCLib.utils.get_version_list()
        else:
            MCVerList = GetReleases()
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
            if not Config.ShowHistorical and RealistikDash[0] == "b":
                pass
            else:
                McVers.append(RealistikDash)

    McVers = natsorted(McVers)
    McVers.reverse()
    McVers.insert(0, Config.Config["LastSelected"]) #using a bug in ttk to our advantage
    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *McVers)
    Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)

#The creation of the main window
if __name__ == '__main__':
    if Config.RPCEnable:
        RPC = Presence(Config.ClientId)
        RPC.connect()
        DefaultPresence()
    ConfigLoad()
    MainWindow = ThemedTk(theme=Config.Theme)
    Update()
    #Styles
    s = ttk.Style()
    s.configure('TButton', background=Config.FG_Colour, fieldbackground=Config.FG_Colour)
    s.configure('TCheckbutton', background=Config.BG_Colour, foreground="white")
    s.configure('TEntry', fieldbackground=Config.FG_Colour, background=Config.FG_Colour)

    MainWindow.configure(background=Config.BG_Colour) # sets bg colour
    MainWindow.title("PyMyMC") # sets window title
    if System == "Windows":
        #other systems dont use ico
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
    Username_Label.grid(row=5, column=0, sticky=W)

    #Username Entry
    US_EntryText = StringVar() #
    Username_Entry = ttk.Entry(MainWindow, width=Config.EntryLen, textvariable=US_EntryText)
    US_EntryText.set(Config.Config["Email"]) #inserts config email here
    Username_Entry.grid(row=6, column = 0, sticky=W)

    #Password Label
    Password_Label = Label(MainWindow, text="Password:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Password_Label.grid(row=7, column=0, sticky=W)

    #Password Entry
    Password_Entry = ttk.Entry(MainWindow, width=Config.EntryLen, show="*")
    Password_Entry.grid(row=8, column = 0, sticky=W)

    #Play Button
    Play_Button = ttk.Button(MainWindow, text="Play!", width=Config.BoxWidth, command = Play)
    Play_Button.grid(row = 11, column=0, sticky = W)

    #Install Button
    Install_Button = ttk.Button(MainWindow, text="Download!", width=Config.BoxWidth, command = Install)
    Install_Button.grid(row = 11, column=0, sticky = E)

    #Version Label
    Version_Label = Label(MainWindow, text="Version:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Version_Label.grid(row=9, column=0, sticky=W)

    #Im just trying to get something working
    Empty = []

    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *Empty)
    Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)

    #Config Button
    Config_Button = ttk.Button(MainWindow, text="Config",  width=Config.BoxWidth, command = ConfigWindowFunc)
    Config_Button.grid(row = 11, column=0)

    #Remember Me Checkbox
    RememberMe_Var = IntVar() #value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(MainWindow, text="Remember me", variable=RememberMe_Var)
    RememberMe_Checkbox.grid(row=10, column=0, sticky=E)

    #Download Progress Bar
    Download_Progress = ttk.Progressbar(MainWindow, length=Config.BarLen)
    Download_Progress.grid(row=12, column=0)

    PopulateThread = Thread(target=PopulateRoot)
    #PopulateThread.start()
    if True:
        #i broke something
        try:
            #So the launcher still works if internet not here
            if Config.ShowHistorical:
                MCVerList = MCLib.utils.get_version_list()
            else:
                MCVerList = GetReleases()
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
                if not Config.ShowHistorical and RealistikDash[0] == "b":
                    pass
                else:
                    McVers.append(RealistikDash)

        McVers = natsorted(McVers)
        McVers.reverse()
        McVers.insert(0, Config.Config["LastSelected"]) #using a bug in ttk to our advantage
        ListVariable = StringVar(MainWindow)
        Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *McVers)
        Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
        Ver_List.grid(row=10, column=0, sticky=W)
    MainWindow.mainloop()