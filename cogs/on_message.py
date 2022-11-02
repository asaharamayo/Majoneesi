import discord
from discord import app_commands
from discord.ext import commands
import re

class HiCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,message):
        x = message.content.casefold()
        Triggers = {
            'im ', 'i am ', "i'm "
        }
        
        for y in Triggers:
            if y in x:
                await message.channel.send('Hi ' + str(x.split(y)[1] + ' \N{SKULL}'))
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HiCog(bot))