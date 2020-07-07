import requests 
import platform
from tqdm import tqdm
import os
from pyunpack import Archive
import os.path
import shutil
import subprocess
import psutil

# checks what operation system the user runs on
def osCheck():
    os = platform.system()

    if os == "Linux": # linux 
        return False
    elif os == "Windows": # windows
        return True
    elif os == "Darwin": # osx
        print("TF2 Classic does not support macos at the moment.")
        exit(-1)
    else:
        return # this should never happen
        
def downloadFiles():

    print("Downloading files from tf2c.switchbla.de ...")

    url = "https://tf2c.switchbla.de/classic.7z"
    r = requests.get(url, stream=True)

    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte

    total = int(r.headers.get('content-length'))
    t= tqdm(r.iter_content(), total=total, unit='iB', unit_scale=True)
    with open('classic.7z', 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong")
    


def unzipFiles():
    print("Unzipping classic.7z..")
    Archive("classic.7z").extractall("./")
    print("Done!")


if osCheck: # on windows
    import winreg
    from winreg import HKEY_CURRENT_USER
else:
    # import linux library or something 
    exit(0)

def moveFiles():
    path = ""
    if osCheck:
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_READ)
            path = winreg.QueryValueEx(registry_key, r"SourceModInstallPath")
            winreg.CloseKey(registry_key)
            
        except WindowsError:
            return None
    else:
        if os.path.exists("~/.steam/steam/steamapps/sourcemods"):
            path = "~/.steam/steam/steamapps/sourcemods"

    if os.path.exists(path):
        print("Found sourcemods folder, moving files..")
        shutil.move("tf2classic", path)
        print("Done!")
    else:  
        print("sourcemods folder could not be found, can you input the full path of the sourcemods folder?")
        user_path = input("Please input the full path of the sourcemods folder: ")
        if os.path.exists(user_path):
            print("Moving files..")
            shutil.move("tf2classic", user_path)


def getPid(name):
    for proc in psutil.process_iter():
        
        if proc.name() == name:
            return proc.pid

def restartSteam():
    print("restarting steam..")
    os.kill(getPid("steam.exe"), 9)
    print("Sucessfully installed TF2C!")
    exit(0)


osCheck()
downloadFiles()
unzipFiles()
moveFiles()
restartSteam()