from discord.ext import commands, tasks
from discord import app_commands, utils
import asyncio
import datetime
from datetime import timedelta
from dateutil import tz
from time import sleep

class ClockCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.clock_loop.start()

    @tasks.loop(minutes=30)
    async def clock_loop(self):
        timezones = {
        'Mayo': 'Asia/Hong_Kong',
        'Yimi': 'Europe/Helsinki',
        'Aki': 'America/New_York',
        'Sora': 'America/Los_Angeles'
        }
        channelids = {
        'Mayo': 1036329698600431657,
        'Yimi': 1036331077586919615,
        'Aki': 1036331099946762363,
        'Sora': 1036331148453892196
        }
          
        for x in timezones:
            y = tz.gettz(timezones[f'{x}'])
            time = datetime.datetime.now(tz=(y))
            await self.bot.get_channel(channelids[f'{x}']).edit(name = f' ♡ {time.strftime("%I:%M %p")} ♡ {x}')
            sleep(3)   
       
    @clock_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()
        
        a = int(datetime.datetime.min)
        n = int(0)
        range_min = 15*n
        range_max = 15*(n+1)
        while n <= 4:
            if a > range_min and a < range_max:
                min_to_next_q = range_max - a
            else:
                n = n + 1
            continue
        
        sleep(60*min_to_next_q)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClockCog(bot))