#✿---✿---✿---✿Imports✿---✿---✿---✿

import os
import discord
from discord.ext import commands

#✿---✿---✿---✿Configurations✿---✿---✿---✿

prefix = ',,'
token = 'MTAzNjI4NTE0NzAwMTE0NzQzMw.GGsRKO.ygEpEpzydUMTWgrY0m8Q3eY8ljMwHG6PJsYYdI'

#✿---✿---✿---✿Codes✿---✿---✿---✿

class Client(commands.Bot):
    def __init__ (self):
        intents = discord.Intents.default()
    #✿intents settings✿
        intents.message_content = True
        intents.presences = True
        intents.members = True
        super().__init__(command_prefix = prefix, intents=intents)
    
    #✿loading in cogs✿
    async def setup_hook(self):
        await self.load_cogs(client=self, directory="./cogs")
    
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

client=Client()
client.run(token)