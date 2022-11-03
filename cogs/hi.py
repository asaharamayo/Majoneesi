import discord
from discord import app_commands
from discord.ext import commands
import re

class HiCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message, /) -> None:
        pattern: re.Pattern[str] = re.compile(r"\b(?:im|i am|i\'m)\b\s(.*)")
        a = message.content.casefold()
        dad = 'dad'
        if match := pattern.search(a):
            if dad in a:
                await message.channel.send(f'Hi daddy allowance <:die_you:1037445906729017365>', reference=message)
            else:
                len_show = message.content[-len(match[1]):]
                await message.channel.send(f"Hi {len_show} \N{SKULL}", reference=message)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HiCog(bot))