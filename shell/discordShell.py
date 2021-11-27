from shell.helpMenu import Menu as HelpMenu
from shell.tools import *
import discord

class DCShell:
    def __init__(self) -> None:
        self.hMenu = HelpMenu()
        self.myIp = get_ip()

    async def process(self, message) -> None:
        cmd = message.content.split(" ")
        if cmd[0] == "ping":
            await message.reply("Pong!")
        elif cmd[0] == "check":
            await message.channel.send("checked")
        elif cmd[0] == "help":
            if len(cmd) > 1:
                await message.reply(embed=self.hMenu.displayForCommand(cmd[1]))
            else:
                await message.reply(embed=self.hMenu.display())
        elif cmd[0] in ["ip", "ipconfig", "ipinfo", "viewip", "showip"]:
            await message.reply("This is my public IP: "+self.myIp)
        elif cmd[0] in ["info", "geolocate", "geolocation", "infomenu"]:
            await message.reply(embed=discord.Embed(
                title="📍 Info Menu 📍",
                description="",
                color=discord.Color.from_rgb()
            ))
        elif cmd[0] == ["ftp", "ftp+", "ftpshell", "shellftp"]:
            pass
        elif cmd[0] in ["kill", "stop"]:
            await message.reply("Killing this shell...")
            exit()
        elif cmd[0] == "author":
            await message.reply(embed=self.hMenu.authorInfo())
        else:
            await message.reply("Invalid Command")