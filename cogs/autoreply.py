import discord
from discord import app_commands
from discord.ext import commands
import re


class AutoCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        
    @commands.Cog.listener()
    async def on_message(self,message: discord.Message, /) -> None:
        pattern: re.Pattern[str] = re.compile(r"\b(?:im|i am|i\'m|I\’m)\b\s(.*)", flags=re.I)
        a = await message.content.casefold()
        dad = self.bot.config["auto_resp"]["hi_excep_kw"]
        if match := pattern.search(message.content):
            if not message.author.bot and self.bot.config["auto_resp"]["hi_trigger"] == True:
                if dad in a:
                    await message.channel.send(self.bot.config["auto_resp"]["hi_excep_resp"], reference=message)
                else:
                    await message.channel.send(f'Hi {match[1]} \N{SKULL}', reference=message)
        ily: re.Pattern[str] = re.compile(r"\b(?:love|luv|ily)\b\s(.*)", flags=re.I)
        mayo = 'mayo'
        if xxx := ily.search(message.content) and mayo in message.content.casefold() and not message.author.bot and self.bot.config["auto_resp"]["ily_trigger"] ==True:
            await message.channel.send(f'{self.bot.config["auto_resp"]["ily_resp"]} ♡ <@!{message.author.id}>', reference=message)
        if '69' in message.content.casefold() and not message.author.bot and self.bot.config["auto_resp"]["69_trigger"] ==True:
            await message.add_reaction('\U0001f602')
        if 'hi dad' in message.content.casefold() and not message.author.bot and self.bot.config["auto_resp"]["hi_trigger"] ==True:
            await message.channel.send(self.bot.config["auto_resp"]["resp_excep_resp"], reference=message)
        
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoCog(bot))