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
        self.clock_loop.change_interval(time = datetime.time(minute=self.bot.config["tzclock"][0]["interval"]))
        self.clock_loop.start()

    @tasks.loop()
    async def clock_loop(self):
        j = ''
        k = ''
        l = ''
        for y in range(1,5):
            j += f'{self.bot.config["tzclock"][1][str(y)]["tz"]},'
            k += f'{self.bot.config["tzclock"][1][str(y)]["tz_channelids"]},'
            l += f'{self.bot.config["tzclock"][1][str(y)]["name"]},'
        timezones = j[:-1].split(",")
        channelids = k[:-1].split(",")
        names = l[:-1].split(",")
          
        for t in range(0,4):
            y = tz.gettz(timezones[t])
            time = datetime.datetime.now(tz=(y))
            for u in range (1,5):
                if t == self.bot.config["tzclock"][1][str(u)]["tz"]:
                    await self.bot.get_channel(channelids[(u-1)]).edit(name = f' ♡ {time.strftime("%I:%M %p")} ♡ {names[(u-1)]}')
                    sleep(3)
                
       
    @clock_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()
        
        a = int(datetime.datetime.now().strftime('%M'))
        n = ""
        for n in range (0,4):
            range_min = 15*n
            range_max = 15*(n+1)
            if a > range_min and a <= range_max:
                global min_to_next_q
                min_to_next_q = range_max - a
                break
            else:
                n = (n + 1)
                continue
        
        await asyncio.sleep(60*min_to_next_q)
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClockCog(bot))