from shell.helpMenu import Menu, Command
import discord

class FTPShell:
    def __init__(self) -> None:
        self.active = False
        self.hMenu = Menu({
            "ping": Command("This **help menu**"),
            "exit": Command("**Exit** the **FTP+** shell", (224, 27, 27))
        })

    async def process(self, message, cmd) -> None:
        if cmd == "ping":
            await message.reply("Pong! (from FTP+)")
        elif cmd == "exit":
            self.active = False
        else:
            await message.reply("Invalid Command")