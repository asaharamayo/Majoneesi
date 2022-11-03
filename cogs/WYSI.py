import discord
from discord import  utils
from discord.ext import commands, tasks
import re
import datetime
from dateutil import tz
import random
from random import choice

class WYSI_React(commands.Cog):   
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
           
    @commands.command()
    async def WYSI(self, ctx):
        await ctx.send('https://tenor.com/view/aireu-wysi-osu-727-cookiezi-gif-20763403')

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message, /) -> None:
        wysi: re.Pattern[str] = re.compile(r"\b(?:WYSI|when you see it)\b", flags=re.I)
        ayo: re.Pattern = re.compile(r"7\D?2\D?7\D?")
        emoji = ('\U0001f1fc','\U0001f1fe','\U0001f1f8','\U0001f1ee','\U0001f446')
        if match := wysi.search(message.content):
            if message.author.bot:
                return
            else: 
                for j in emoji:
                    await message.add_reaction(j)  
        elif match := ayo.search(message.content):
            if message.author.bot:
                return
            else: 
                for j in emoji:
                    await message.add_reaction(j)

class WYSI_loop(commands.Cog):
    timezones = ('Asia/Hong_Kong','Europe/Helsinki','America/New_York','America/Los_Angeles')
    hours = 7, 19 
    pairs = {
        'Asia/Hong_Kong':'231906328954535948',
        'Europe/Helsinki': '277850351841837066',
        'America/New_York': '259747383699701760',
        'America/Los_Angeles': '182293404435218432'
        }   
        
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.ping_loop.start()
        self.rand = choice(WYSI_loop.timezones)
        self.h = choice(WYSI_loop.hours)
        self.x = random.randrange(0,4)

    def cog_unload(self):
        self.ping_loop.stop()
    
    initial = True

    @commands.command(hidden=True)
    @commands.is_owner()
    async def random(self, ctx):
        self.rand = choice(WYSI_loop.timezones)
        self.h = choice(WYSI_loop.hours)
        self.x = random.randrange(0,4)
        await ctx.send(f'Ramdomized as {self.rand} ; {self.h} ; {self.x} ; {datetime.datetime.now()} ♡ ')
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def nWYSI(self, ctx):
        await ctx.send(f'Last ramdomized as {self.rand} ; {self.h} ; {self.x} ; {datetime.datetime.now()} ♡ ')

    @tasks.loop()
    async def ping_loop(self):
        if self.initial == True: 
            self.initial == False
            return
        else:
            nuts = 1030582725851234404
            await self.bot.get_channel(nuts).send('https://tenor.com/view/aireu-wysi-osu-727-cookiezi-gif-20763403')
            await self.bot.get_channel(nuts).send('<@' + str(self.pairs[self.rand]) +'>')
        year_now = datetime.datetime.now().year
        month_now = datetime.datetime.now().month
        day_now = datetime.datetime.now().day
        rand_day = day_now + self.x
        next_run_time = datetime.datetime(year=year_now, month=month_now, day=rand_day, hour=self.h, minute=27, tzinfo = tz.gettz(self.rand))
        await utils.sleep_until(next_run_time)
        await self.random(self)

    @ping_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WYSI_React(bot))
    await bot.add_cog(WYSI_loop(bot))