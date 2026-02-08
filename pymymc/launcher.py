from __future__ import annotations

import glob
import hashlib
import json
import os
import pathlib
import platform
import random
import subprocess
import traceback
from datetime import datetime
from threading import Thread
from tkinter import E
from tkinter import IntVar
from tkinter import Label
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import ttk
from tkinter import W
from typing import Literal
from typing import TypedDict

import minecraft_launcher_lib as MCLib
import requests
from colorama import Fore
from colorama import init
from natsort import natsorted
from pypresence import Presence
from ttkthemes import ThemedTk

from pymymc import constants

ASCII = r""" _____       __  __       __  __  _____
 |  __ \     |  \/  |     |  \/  |/ ____|
 | |__) |   _| \  / |_   _| \  / | |
 |  ___/ | | | |\/| | | | | |\/| | |
 | |   | |_| | |  | | |_| | |  | | |____
 |_|    \__, |_|  |_|\__, |_|  |_|\_____|
         __/ |        __/ |
        |___/        |___/   by RealistikDash
"""
init()  # initialises colorama
COLOURS = (
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.BLUE,
    Fore.WHITE,
    Fore.CYAN,
    Fore.GREEN,
)
SYSTEM = platform.system()


VersionTypes = Literal["snapshot", "release", "old_beta"]


class MinecraftRelease(TypedDict):
    """Typing for a Minecraft version manifest JSON resposne."""

    id: str
    type: VersionTypes
    url: str
    time: str
    releaseTime: str


class Config:
    # Why a class? I dont know
    config = {}  # this is loaded later on

    version = "0.1.8MC"
    minecraft_dir = ""

    has_internet = True
    show_historical = False


def save_config() -> None:
    """Saves the current state of the config into the file."""

    with open("config.json", "w") as f:
        json.dump(Config.config, f, indent=4)


def log_coloured(content: str, colour: str) -> None:
    """Prints a message to the console, prefixing the message with `colour` and
    ending it with a colour reset."""

    print(colour + content + Fore.RESET)


def log_info(content: str) -> None:
    """Logs `content` to console with the severity `INFO`."""

    log_coloured(f"[{format_time()}] {content}", Fore.BLUE)


def log_warning(content: str) -> None:
    """Logs `content` to console with the severity `WARNING`."""

    log_coloured(f"[{format_time()}] {content}", Fore.YELLOW)


def log_error(content: str) -> None:
    """Logs `content` to console with the severity `ERROR`."""

    log_coloured(f"[{format_time()}] {content}", Fore.RED)


def message_box(title: str, content: str) -> None:
    """Creates a message box"""
    # msg_thread = Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, content, title, style,))
    # msg_thread.start() #non blocking?
    msg_thread = Thread(
        target=messagebox.showinfo,
        args=(
            title,
            content,
        ),
    )
    msg_thread.start()
    log_info(content)


def error_box(title: str, content: str) -> None:
    """Creates an error dialogue box"""
    msg_thread = Thread(
        target=messagebox.showerror,
        args=(
            title,
            content,
        ),
    )
    msg_thread.start()
    log_error(content)


def warning_box(title: str, content: str) -> None:
    """Creater a warning dialogue box"""
    msg_thread = Thread(
        target=messagebox.showwarning,
        args=(
            title,
            content,
        ),
    )
    msg_thread.start()
    log_warning(content)


def config_window() -> None:
    """Creates an advanced config window"""
    # i know this is not supposed to be how you do it but "it just works"

    def handle_config_close() -> None:
        """Function ran when the config window is closed"""
        config_win.destroy()
        set_default_presence()

    def apply_config() -> None:
        mc_path = mc_path_var.get()
        dram_value = dram_var.get()
        forget_me = int(remember_me_var.get())

        is_valid_dram = True

        try:
            dram_value = int(dram_value)
            if dram_value <= 0:
                is_valid_dram = False
        except Exception:
            is_valid_dram = False  # nicest way i know of doing this

        if is_valid_dram:
            if forget_me == 1:
                Config.config["Email"] = ""
                Config.config["UUID"] = ""
                Config.config["AccessToken"] = ""
                Config.config["Username"] = ""
            Config.config["JVMRAM"] = dram_value
            if SYSTEM == "Windows":
                if mc_path[-1] != "\\":
                    mc_path = mc_path + "\\"
            else:
                # other systems use / instead of \
                if mc_path[-1] != "/":
                    mc_path = mc_path + "/"
            if premium_var.get() == 1:
                Config.config["Premium"] = True
            if premium_var.get() == 0:
                Config.config["Premium"] = False
            if historical_var.get() == 0:
                Config.config["OnlyReleases"] = True
            if historical_var.get() == 1:
                Config.config["OnlyReleases"] = False
            Config.config["MinecraftDir"] = mc_path
            save_config()
            config_load()  # runs config update
            config_win.destroy()
            populate_root()

        else:
            error_box(
                "PyMyMC Error!",
                "The RAM value has to be an integer (full number) over 0.",
            )

    # Discord Rich Presence Update
    if constants.rpc.ENABLED:
        rpc_client.update(
            state="Configuring things...",
            small_image=constants.rpc.CONFIG_IMAGE,
            large_image=constants.rpc.LARGE_IMAGE,
        )
    # Initial window settings
    config_win = Toplevel(main_window)
    config_win.configure(background=constants.ui.BG_COLOUR)  # sets bg colour
    config_win.title("PyMyMC Config")  # sets window title
    config_win.protocol("WM_DELETE_WINDOW", handle_config_close)
    if SYSTEM == "Windows":
        # other systems dont use ico
        main_window.iconbitmap(constants.ui.LOGO_ICON)  # sets window icon
    config_win.resizable(False, False)  # makes the window not resizable

    # WarningLabel
    warning_label = Label(
        config_win,
        text="Warning! These options are for advanced users only!",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    warning2_label = Label(
        config_win,
        text="Proceed with caution!",
        bg=constants.ui.BG_COLOUR,
        fg="yellow",
        font="none 12 bold",
    )
    warning_label.grid(row=0, column=0, sticky=W)
    warning2_label.grid(row=1, column=0, sticky=W)

    # MC Path Label
    mc_path_label = Label(
        config_win,
        text="Minecraft Path:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 11",
    )
    mc_path_label.grid(row=2, column=0, sticky=W)

    # MC Path Entry
    mc_path_var = StringVar()
    mc_path_entry = ttk.Entry(config_win, width=40, textvariable=mc_path_var)
    mc_path_var.set(Config.config["MinecraftDir"])
    mc_path_entry.grid(row=3, column=0, sticky=W)

    # Dedicated RAM Label
    dram_label = Label(
        config_win,
        text="JVM Dedicated RAM:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 11",
    )
    dram_label.grid(row=4, column=0, sticky=W)

    # Dedicated RAM Entry
    dram_var = StringVar()
    dram_entry = ttk.Entry(config_win, width=10, textvariable=dram_var)
    dram_var.set(Config.config["JVMRAM"])
    dram_entry.grid(row=5, column=0, sticky=W)

    gb_label = Label(
        config_win,
        text="GB",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 9",
    )
    gb_label.grid(row=5, column=0, sticky=E)

    # ForgetMe RADIO
    remember_me_var = IntVar()  # value whether its ticked is stored here
    remember_me_checkbox = ttk.Checkbutton(
        config_win,
        text="Forget Me",
        variable=remember_me_var,
    )
    remember_me_checkbox.grid(row=6, column=0, sticky=W)

    # Premium RADIO
    premium_var = IntVar()  # value whether its ticked is stored here
    if Config.config["Premium"]:
        premium_var.set(1)  # sets to whats enabled
    premium_checkbox = ttk.Checkbutton(
        config_win,
        text="Use Premium Minecraft Accounts",
        variable=premium_var,
    )
    premium_checkbox.grid(row=7, column=0, sticky=W)

    # Show Historical
    historical_var = IntVar()
    if not Config.config["OnlyReleases"]:
        historical_var.set(1)
    historical_checkbox = ttk.Checkbutton(
        config_win,
        text="Show non-release versions",
        variable=historical_var,
    )
    historical_checkbox.grid(row=8, column=0, sticky=W)

    # Apply Button
    apply_button = ttk.Button(
        config_win,
        text="Apply",
        width=constants.ui.BOX_WIDTH,
        command=apply_config,
    )
    apply_button.grid(row=9, column=0, sticky=W)

    # Cancel Button
    cancel_button = ttk.Button(
        config_win,
        text="Cancel",
        width=constants.ui.BOX_WIDTH,
        command=config_win.destroy,
    )
    cancel_button.grid(row=9, column=0, sticky=E)


def install(play_after: bool = False) -> None:
    """Installs minecraft"""
    # version = "1.14.4" #later change it into a gui list # i did
    version = list_var.get()

    is_installed = os.path.exists(Config.minecraft_dir + f"versions\\{version}\\")
    if is_installed:
        message_box(
            "PyMyMC Info!",
            "This version is already installed! Press play to play it!",
        )

    elif not Config.has_internet:
        error_box(
            "PyMyMC Error!",
            "An internet connection is required for this action!",
        )

    else:
        message_box(
            "PyMyMC Info!",
            "Downloading started! If you pressed play to download, the program will freeze.",
        )
        callback = {
            "setStatus": set_status_handler,
            "setProgress": set_progress_handler,
            "setMax": set_max_handler,
        }
        # MCLib.install.install_minecraft_version(version, Config.minecraft_dir, callback=callback)
        dl_thread = Thread(
            target=MCLib.install.install_minecraft_version,
            args=(
                version,
                Config.minecraft_dir,
            ),
            kwargs={"callback": callback},
        )
        dl_thread.start()
        if play_after:
            dl_thread.join()
            play()


# TODO: Rewrite
def play() -> None:
    """Function that is done when the play button is pressed"""
    # Note 25/12/19 | Deal with sessions expiring
    def update_play_rpc(version: str, username: str, is_premium: bool) -> None:
        """Updates the rich presence so i dont have to copy and paste the same code on premium and nonpremium"""
        # Checks if the user is playing vanilla mc or modded for RPC icon
        if constants.rpc.ENABLED:
            is_vanilla = True
            mc_versions = MCLib.utils.get_version_list()
            version_ids = []
            for thing in mc_versions:
                version_ids.append(thing["id"])
            if version in version_ids:
                is_vanilla = True
            else:
                is_vanilla = False
            if is_vanilla:
                small_icon = constants.rpc.VANILLA_IMAGE
            else:
                small_icon = constants.rpc.MODDED_IMAGE

            # Details text
            if not is_premium:
                premium_state = ", non-premuim"
            else:
                premium_state = ""
            rpc_client.update(
                state=f"Playing Minecraft {version}",
                large_image=constants.rpc.LARGE_IMAGE,
                small_image=small_icon,
                details=f"Playing as {username}{premium_state}",
            )

    email = username_entry.get()
    password = password_entry.get()
    version = list_var.get()
    remember_me = remember_me_var.get() == 1

    # NonPremium code
    if email == "":
        warning_box("PyMyMC Error!", "Username cannot be empty!")
    else:
        if Config.config["Premium"]:
            # Attempt to make a username out of the email.
            email, _ = email.split("@")
        options = {
            "username": email,
            "uuid": str(hashlib.md5(str.encode(email)).digest()),
            "token": "",
            "launcherName": "PyMyMC",
            "gameDirectory": Config.minecraft_dir,
            "jvmArguments": [f"-Xmx{Config.config['JVMRAM']}G"],
        }

        if remember_me:
            Config.config["Email"] = email

        Config.config["LastSelected"] = version
        save_config()

        command = MCLib.command.get_minecraft_command(
            version,
            Config.minecraft_dir,
            options,
        )
        main_window.destroy()
        update_play_rpc(version, email, False)

        subprocess.call(command)
        # message_box("PyMyMC", "Thank you for using PyMyMC!") #Temporarily disabled as it would create an empty tk window


if SYSTEM == "Windows":
    MC_DIR = os.getenv("APPDATA") + "\\.minecraft\\"
else:
    # I dont know if this will work with macs or not
    MC_DIR = str(pathlib.Path.home()) + "/.minecraft/"

EXAMPLE_CONFIG = {
    "IsExample": False,
    "MinecraftDir": MC_DIR,
    "Email": "",
    "UUID": "",
    "AccessToken": "",
    "JVMRAM": 2,  # in GB
    "Premium": True,
    "LastSelected": "1.15.1",
    "OnlyReleases": True,
}

# TODO: Full rewrite.
def config_load() -> None:
    """Function to load/make new config"""
    # JSONConfig = JsonFile.GetDict("config.json")
    # if JSONConfig == {}:
    #    JSONConfig = ExampleConfig
    #    JsonFile.SaveDict(JSONConfig, "config.json")
    # if JSONConfig["IsExample"] == True:
    #    Config.config = ExampleConfig
    # else:
    #    Config.config = JSONConfig

    if not os.path.exists("config.json"):
        base_cfg = EXAMPLE_CONFIG.copy()
    else:
        with open("config.json") as f:
            base_cfg = json.load(f)

        if base_cfg == {}:
            base_cfg = EXAMPLE_CONFIG.copy()

    Config.config = base_cfg

    Config.minecraft_dir = Config.config["MinecraftDir"]

    # Making older configs compatible with newer ones
    if "JVMRAM" not in list(Config.config.keys()):
        # for reuse of older configs
        Config.config["JVMRAM"] = 2

    if "Premium" not in list(Config.config.keys()):
        Config.config["Premium"] = True

    if "LastSelected" not in list(Config.config.keys()):
        Config.config["LastSelected"] = "1.15.1"

    if "OnlyReleases" not in list(Config.config.keys()):
        Config.config["OnlyReleases"] = True
        Config.show_historical = False

    # Only Releases Fixes. Not cleanest way of doing it but gets the job done
    if Config.config["OnlyReleases"]:
        Config.show_historical = False
    else:
        Config.show_historical = True

    save_config()
    Config.has_internet = check_internet()


INTERNET_TEST_URL = "https://1.1.1.1/"


def check_internet() -> bool:
    """Checks for a working internet connection"""
    try:
        resp = requests.get(INTERNET_TEST_URL, timeout=1)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False


def exit_handler() -> None:
    """Function ran on the closing of the tk mainwindow"""
    main_window.destroy()
    exit()


def set_status_handler(status: str) -> None:
    download_progress["value"] = 0
    print(status)


def set_progress_handler(status: int) -> None:
    download_progress["value"] = int(status)


def set_max_handler(status: int) -> None:
    download_progress["maximum"] = int(status)


def get_release_list() -> list[MinecraftRelease]:
    """Returns a list of all full mc releases"""
    releases_res = requests.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json",
    ).json()

    return [ver for ver in releases_res["versions"] if ver["type"] == "release"]


def format_time(format="%H:%M:%S") -> str:
    """Formats the current time"""
    return datetime.now().strftime(format)


def set_default_presence():
    """Sets the default presence"""
    if constants.rpc.ENABLED:
        rpc_client.update(
            state="In the main menu.",
            large_image=constants.rpc.LARGE_IMAGE,
            small_image=constants.rpc.ROOT_IMAGE,
        )


def populate_root() -> None:
    """Populates the fields in this function to make the window show up faster"""
    print("Populating...")
    if Config.config["Premium"]:
        username_label["text"] = "Email"
    else:
        username_label["text"] = "Username:"

    # Version list
    minecraft_versions = fetch_versions()
    minecraft_versions.insert(
        0,
        Config.config["LastSelected"],
    )  # using a bug in ttk to our advantage
    list_var = StringVar(main_window)

    # global ver_list
    # ver_list = ttk.OptionMenu(main_window, list_var, *minecraft_versions)
    # ver_list.configure(width=Config.ListLen) #only way i found of maintaining same width
    # ver_list.grid(row=10, column=0, sticky=W)


def fetch_versions() -> list[str]:
    """Returns a list strings of all the available versions."""

    # Fetch all available releases from Mojang.
    try:
        releases = get_release_list()
    except Exception:
        log_error(
            "Failed fetching releases from web with error:\n" + traceback.format_exc(),
        )
        releases = []

    versions = [release["id"] for release in releases]

    # Fetch all currently installed versions.
    version_folders = glob.glob(Config.minecraft_dir + "versions/*/")

    for version_dir in version_folders:
        # Cursed way to fetch the version name from folder name.
        version_name = version_dir.split("\\" if SYSTEM == "Windows" else "/")[-2]
        if version_name not in versions:
            versions.append(version_name)

    # Filtering.
    for version in versions:
        # Remove betas is show historical is disabled.
        if (not Config.show_historical) and version[0] == "b":
            versions.remove(version)

    # Sorting.
    versions = natsorted(versions, reverse=True)
    return versions


def main() -> None:
    """The creation of the main window."""
    global main_window, list_var, username_entry, password_entry
    global remember_me_var, download_progress, rpc_client, username_label, ver_list

    log_coloured(ASCII, random.choice(COLOURS))
    log_info("Checking internet status...")
    config_load()
    if constants.rpc.ENABLED:
        log_info("Configuring the Discord Rich Presence...")
        rpc_client = Presence(constants.rpc.CLIENT_ID)
        rpc_client.connect()
        set_default_presence()
    log_info("Loading themes...")
    main_window = ThemedTk(theme=constants.ui.THEME)
    # Styles
    log_info("Configuring the UI...")
    s = ttk.Style()
    s.configure(
        "TButton",
        background=constants.ui.FG_COLOUR,
        fieldbackground=constants.ui.FG_COLOUR,
    )
    s.configure("TCheckbutton", background=constants.ui.BG_COLOUR, foreground="white")
    s.configure(
        "TEntry",
        fieldbackground=constants.ui.FG_COLOUR,
        background=constants.ui.FG_COLOUR,
    )

    main_window.configure(background=constants.ui.BG_COLOUR)  # sets bg colour
    main_window.title("PyMyMC")  # sets window title
    if SYSTEM == "Windows":
        # other systems dont use ico
        main_window.iconbitmap(constants.ui.LOGO_ICON)  # sets window icon
    main_window.resizable(False, False)  # makes the window not resizable
    main_window.protocol(
        "WM_DELETE_WINDOW",
        exit_handler,
    )  # runs the function when the user presses the X button

    # Logo Image
    logo_image = PhotoImage(file=constants.ui.LOGO_SMALL)
    logo_label = Label(main_window, image=logo_image)
    logo_label["bg"] = logo_label.master["bg"]
    logo_label.grid(row=0, column=0)

    # Info Label
    info_label = Label(
        main_window,
        text=f"PyMyMC {Config.version}",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="Arial 15 bold",
    )
    info2_label = Label(
        main_window,
        text="Made by RealistikDash",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 13",
    )
    info_label.grid(row=2, column=0, sticky=W)
    info2_label.grid(row=3, column=0, sticky=W)

    # Username Label
    username_label = Label(
        main_window,
        text="Email:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    username_label.grid(row=5, column=0, sticky=W)

    # Username Entry
    username_text_var = StringVar()  #
    username_entry = ttk.Entry(
        main_window,
        width=constants.ui.ENTRY_LEN,
        textvariable=username_text_var,
    )
    username_text_var.set(Config.config["Email"])  # inserts config email here
    username_entry.grid(row=6, column=0, sticky=W)

    # Password Label
    password_label = Label(
        main_window,
        text="Password:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    password_label.grid(row=7, column=0, sticky=W)

    # Password Entry
    password_entry = ttk.Entry(main_window, width=constants.ui.ENTRY_LEN, show="*")
    password_entry.grid(row=8, column=0, sticky=W)

    # Play Button
    play_button = ttk.Button(
        main_window,
        text="Play!",
        width=constants.ui.BOX_WIDTH,
        command=play,
    )
    play_button.grid(row=11, column=0, sticky=W)

    # Install Button
    install_button = ttk.Button(
        main_window,
        text="Download!",
        width=constants.ui.BOX_WIDTH,
        command=install,
    )
    install_button.grid(row=11, column=0, sticky=E)

    # Version Label
    version_label = Label(
        main_window,
        text="Version:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    version_label.grid(row=9, column=0, sticky=W)

    # Im just trying to get something working
    empty = []

    list_var = StringVar(main_window)
    ver_list = ttk.OptionMenu(main_window, list_var, *empty)
    ver_list.configure(
        width=constants.ui.LIST_LEN,
    )  # only way i found of maintaining same width
    ver_list.grid(row=10, column=0, sticky=W)

    # Config Button
    config_button = ttk.Button(
        main_window,
        text="Config",
        width=constants.ui.BOX_WIDTH,
        command=config_window,
    )
    config_button.grid(row=11, column=0)

    # Remember Me Checkbox
    remember_me_var = IntVar()  # value whether its ticked is stored here
    remember_me_checkbox = ttk.Checkbutton(
        main_window,
        text="Remember me",
        variable=remember_me_var,
    )
    remember_me_checkbox.grid(row=10, column=0, sticky=E)

    # Download Progress Bar
    download_progress = ttk.Progressbar(main_window, length=constants.ui.BAR_LEN)
    download_progress.grid(row=12, column=0)

    minecraft_versions = fetch_versions()
    minecraft_versions.insert(
        0,
        Config.config["LastSelected"],
    )  # using a bug in ttk to our advantage
    list_var = StringVar(main_window)
    ver_list = ttk.OptionMenu(main_window, list_var, *minecraft_versions)
    ver_list.configure(
        width=constants.ui.LIST_LEN,
    )  # only way i found of maintaining same width
    ver_list.grid(row=10, column=0, sticky=W)

    log_info("Done!")
    main_window.mainloop()


if __name__ == "__main__":
    main()
