import discord
from discord import app_commands
from discord.ext import commands

class UwUCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.bot=client
        
    @commands.command()
    async def uwu(self, ctx):
        await ctx.send(self.bot.config["commands"]["uwu"])

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UwUCog(bot))