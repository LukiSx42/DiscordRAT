from requests import get

def get_ip():
    return get('https://api.ipify.org').content.decode()