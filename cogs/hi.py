import discord
from discord import app_commands
from discord.ext import commands
import re

class HiCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,message):
        a = message.content.casefold()
        dad = 'dad'
        Triggers = {
            'im ', 'i am ', "i'm "
        }
        
        for y in Triggers:
            if y in a and dad in a:
                await message.channel.send('Hi daddy allowance <:die_you:1037445906729017365>', reference=message)
            elif y in a and dad not in a:
                await message.channel.send('Hi ' + str(message.content.split(y)[1] + ' \N{SKULL}'), reference=message)
                break
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HiCog(bot))