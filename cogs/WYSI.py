import discord
from discord import  utils
from discord.ext import commands, tasks
import re
import datetime
from datetime import timedelta
from dateutil import tz
import random
from random import choice

class WYSI_React(commands.Cog):   
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
           
    @commands.command()
    async def WYSI(self, ctx):
        if self.bot.config["WYSI"]["command_trigger"] == True:
            await ctx.send('https://tenor.com/view/aireu-wysi-osu-727-cookiezi-gif-20763403')

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message, /) -> None:
        wysi: re.Pattern[str] = re.compile(r"\b(?:WYSI|when you see it)\b", flags=re.I)
        ayo: re.Pattern = re.compile(r"7\D?2\D?7\D?")
        emoji = ('\U0001f1fc','\U0001f1fe','\U0001f1f8','\U0001f1ee','\U0001f446')
        if self.bot.config["WYSI"]["auto_reply"] == True:
            if match := wysi.search(message.content) and not message.author.bot:
                for j in emoji:
                        await message.add_reaction(j)  
            elif match := ayo.search(message.content) and not message.author.bot:
                for j in emoji:
                    await message.add_reaction(j)

class WYSI_loop(commands.Cog):       
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.j = ''
        for y in range(1,5):
            self.j += f'{self.bot.config["tzclock"][1][str(y)]["tz"]},'
        self.rand = choice(self.j[:-1].split(","))
        self.h = choice((7,19))
        self.x = random.randrange(0,4)
        self.initial = True
        if self.bot.config["WYSI"]["loop"] == True:
            self.ping_loop.start()

    def cog_unload(self):
        self.ping_loop.stop()
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def random(self, ctx):
        self.rand = await choice(self.j[:-1].split(","))
        self.h = await choice((7,19))
        self.x = await random.randrange(0,4)
        if self.bot.config["WYSI"]["loop"] == True:
            await ctx.send(f'Randomized as {self.rand} ; {self.h} ; {self.x} ; {datetime.datetime.now()} ♡ ')
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def nWYSI(self, ctx):
        if self.bot.config["WYSI"]["loop"] == True:
            await ctx.send(f'Last randomized as {self.rand} ; {self.h} ; {self.x} ; next run {datetime.datetime.now()} ♡ ')

    async def random_local(self):
        self.rand = choice(self.j[:-1].split(","))
        self.h = choice((7,19))
        self.x = random.randrange(0,4)

    @tasks.loop()
    async def ping_loop(self):
        year_now = datetime.datetime.now().year
        month_now = datetime.datetime.now().month
        day_now = datetime.datetime.now().day
        if self.initial == True: 
            self.initial = False
            rand_day = day_now + self.x
            next_run_time_1 = datetime.datetime(year=year_now, month=month_now, day=rand_day, hour=self.h, minute=27, tzinfo = tz.gettz(self.rand))
            await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(content = f'1: {next_run_time_1}')
            await self.ping_loop.change_interval(time = next_run_time_1)
            
        elif self.initial == False:
            nuts = self.bot.config["channel_id"]["log"]
            await self.bot.get_channel(nuts).send('https://tenor.com/view/aireu-wysi-osu-727-cookiezi-gif-20763403')
            for z in range(1,5):
                if self.bot.config["tzclock"][1][str(z)]["tz"] == self.rand:
                    await self.bot.get_channel(nuts).send('<@' + self.bot.config["tzclock"][1][str(z)]["user_id"] +'>')
                    break
            await self.random_local()
            rand_day = day_now + self.x
            next_run_time = datetime.datetime(year=year_now, month=month_now, day=rand_day, hour=self.h, minute=27, tzinfo = tz.gettz(self.rand))
            await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(content = f'{next_run_time}')
            await self.ping_loop.change_interval(time = next_run_time)
            

    @ping_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WYSI_React(bot))
    await bot.add_cog(WYSI_loop(bot))