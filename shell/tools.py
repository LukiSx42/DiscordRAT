from socket import gethostname
from requests import get
import json, platform

def get_ip():
    return get('https://api.ipify.org').content.decode()

def get_information():
    info = json.loads(get('http://ipinfo.io/json').content.decode())
    info["hostname"] = gethostname()
    info["os"] = platform.system()+" "+platform.release()
    return info