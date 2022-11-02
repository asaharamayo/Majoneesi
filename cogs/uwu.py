import discord
from discord import app_commands
from discord.ext import commands

class UwUCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        
    @commands.command()
    async def uwu(self, ctx):
        await ctx.send(f"Oopsie UwU")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UwUCog(bot))