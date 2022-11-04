#✿---✿---✿---✿Imports✿---✿---✿---✿

import os
import discord
import logging
from discord import app_commands
from discord.ext import commands

#✿---✿---✿---✿Configurations✿---✿---✿---✿

prefix = ',,'
token = 'MTAzNjI4NTE0NzAwMTE0NzQzMw.GGsRKO.ygEpEpzydUMTWgrY0m8Q3eY8ljMwHG6PJsYYdI'
owner_id = 231906328954535948
handler = logging.FileHandler(filename = 'majoneesi.log', encoding = 'utf-8', mode='w')

#✿---✿---✿---✿Codes✿---✿---✿---✿

class Mayo(commands.Bot):
    def __init__ (self):
        intents = discord.Intents.default()
    #✿intents settings✿
        intents.message_content = True
        intents.presences = True
        intents.members = True
        intents.reactions = True
        activity = discord.Game(name="osu! for 7 hours")
        super().__init__(command_prefix = prefix, intents=intents, activity=activity, owner_id = owner_id)
    
    #✿loading in cogs✿
    async def setup_hook(self):
        await self.load_cogs(client=self, directory="./cogs")
        pre_load = 'cogload'
        await self.load_extension(f"{pre_load}")
            
    async def load_cogs(self, client, directory: str) -> None:
        os.chdir(directory)
        base=os.getcwd()
        for x in os.listdir():
            if x.endswith('.py'):
                await self.load_extension(f"cogs.{x[:-3]}")
    
    #✿on ready message
    async def on_ready(self):
        print(f' ♡ Logged in as {client.user} ♡ ')
        print('(´• ᴗ •`✿)')

client=Mayo()
client.run(token, log_handler = None)