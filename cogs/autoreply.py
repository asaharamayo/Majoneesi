import discord
from discord import app_commands
from discord.ext import commands
import re

class AutoCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message, /) -> None:
        pattern: re.Pattern[str] = re.compile(r"\b(?:im|i am|i\'m)\b\s(.*)", flags=re.I)
        a = message.content.casefold()
        dad = 'dad'
        if match := pattern.search(message.content):
            if dad in a:
                await message.channel.send(f'Hi daddy allowance <:die_you:1037445906729017365>', reference=message)
            else:
                await message.channel.send(f'Hi {match[1]} \N{SKULL}', reference=message)
        ily: re.Pattern[str] = re.compile(r"\b(?:i love you|i luv you|ily|i luv u|i love u)\b\s(.*)", flags=re.I)
        mayo = 'mayo'
        if match := ily.search(message.content) and mayo in message.content.casefold():
            if message.author.bot:
                return
            else:
                await message.channel.send(f'I love you too <@!{message.author.id}> ♡ ', reference=message)
        
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoCog(bot))