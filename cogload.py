import os
import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx):
        input = str(ctx.message.content.split(" ")[1])
        try:
            await self.bot.load_extension(f"cogs.{input}")
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e} \N{SKULL}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx):
        input = str(ctx.message.content.split(" ")[1])
        try:
            await self.bot.unload_extension(f"cogs.{input}")
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e} \N{SKULL}')
        else:
            await ctx.send('\N{OK HAND SIGN}')
 
    async def reload_cogs(self, client, directory: str) -> None:
        os.chdir(directory)
        base=os.getcwd()
        for x in os.listdir():
            if x.endswith('.py'):
                await self.bot.reload_extension(f"cogs.{x[:-3]}")
                     
    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload_all(self, ctx):
        await self.reload_cogs(client=self, directory="./")
        await ctx.send('\N{OK HAND SIGN}') 
       

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))