import discord

class Command:
    def __init__(self, description, color=(10, 196, 247), aliases=[], usage=None) -> None:
        self.description = description
        self.aliases = aliases
        self.color = color
        self.usage = usage

class Menu:
    def __init__(self) -> None:
        self.helpMenu = {
            "ping": Command("See if the RAT is running in this channel\n + Some small **latency info**", (34, 218, 25)),
            "kill": Command("**Kill** the RAT", (224, 27, 27), ["stop"]),
            "ip": Command("Get the **public IP** address of the client", (216, 25, 218), ["ipconfig", "ipinfo", "viewip", "showip"]),
            "info": Command("Get all **information** about the client", (227, 222, 15), ["geolocate", "geolocation", "infomenu"]),
            "ftp": Command("Get an **FTP+ shell** from the client", (15, 227, 143), ["ftp+", "ftpshell", "shellftp"])
        }
        self.allAliases = {}
        for cmd in self.helpMenu.keys():
            for alias in self.helpMenu[cmd].aliases:
                self.allAliases[alias] = cmd

    def display(self) -> discord.Embed:
        return discord.Embed(
            title="📘 Help Menu 📘",
            description="__**Here is a list of all commands:**__\n`"+"`, `".join(self.helpMenu.keys())+"`",
            color=discord.Color.from_rgb(10, 196, 247)
        ).set_footer(text="Run 'help <COMMAND>' for more information")
    
    def displayForCommand(self, cmd) -> discord.Embed:
        if cmd not in self.helpMenu.keys():
            if cmd not in self.allAliases.keys():
                return discord.Embed(
                    title="📘 Not Found 📘",
                    description="The command `"+cmd+"` does **not** exist...",
                    color=discord.Color.from_rgb(224, 27, 27)
                ).set_footer(text="For a list of command run 'help'")
            else:
                cmd = self.allAliases[cmd]
        command = self.helpMenu[cmd]
        menu = discord.Embed(
            title="📘 "+cmd[0].upper()+cmd[1:]+" 📘",
            color=discord.Color.from_rgb(command.color[0], command.color[1], command.color[2])
        ).add_field(name="Description", value=command.description, inline=False)
        if command.usage != None:
            menu.add_field(name="Usage", value=command.usage)
        if len(command.aliases) > 0:
            menu.add_field(name="Aliases", value="`"+"`, `".join(command.aliases)+"`", inline=False)
        return menu

    def authorInfo(self) -> discord.Embed:
        return discord.Embed(
            title="LukiS",
            url="https://github.com/LukiSx420",
            description="This RAT was coded by **LukiS**\n > Discord: LukiS#1430\n > GitHub: LukiSx420",
            color=discord.Color.from_rgb(93, 0, 221)
        ).set_thumbnail(url="https://avatars.githubusercontent.com/u/61755983?v=4")