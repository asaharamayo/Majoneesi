#✿---✿---✿---✿Imports✿---✿---✿---✿

import os
import discord
import logging
from discord import app_commands
from discord.ext import commands
import tomli

handler = logging.FileHandler(filename = 'majoneesi.log', encoding = 'utf-8', mode='w')

#✿---✿---✿---✿Codes✿---✿---✿---✿

class Mayo(commands.Bot):
    config = {}
    def __init__ (self):
        intents = discord.Intents.default()
    #✿intents settings✿
        intents.message_content = True
        intents.presences = True
        intents.members = True
        intents.reactions = True
        self.config = tomli.loads(open("./config.toml").read())
        activity = discord.Game(name= Mayo.config["main"]["activity"])
        super().__init__(command_prefix = Mayo.config["main"]["prefix"], intents=intents, activity=activity, owner_id = Mayo.config["user_id"]["owner"])
 
    #✿loading in cogs✿
    async def setup_hook(self):
        await self.load_cogs(client=self, directory="./cogs")
        pre_load = 'cogload'
        await self.load_extension(f"{pre_load}")
            
    async def load_cogs(self, client, directory: str) -> None:
        os.chdir(directory)
        base=os.getcwd()
        for x in os.listdir():
            if x.endswith('.py') and self.config["cogs_load"][str(x)] == True:
                await self.load_extension(f"cogs.{x[:-3]}")
    
    #✿on ready message
    async def on_ready(self):
        print(f' ♡ Logged in as {client.user} ♡ ')
        print('(´• ᴗ •`✿)')

client=Mayo()

client.run(client.config["main"]["token"], log_handler = handler)