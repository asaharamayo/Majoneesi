import os
import discord
from discord import app_commands, Attachment
from discord.ext import commands
import random
import datetime
from PIL import Image

class image_lib(commands.Cog):
    log_chid = 1031578258615042099
    user_id = 231906328954535948

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.file = discord.File(f'{"./image_lib/" + random.choice (os.listdir("./image_lib"))}', filename = "image.png")
        
    async def image_rand(self):
        list = os.listdir("./image_lib")
        image_str = random.choice(list)
        path = "./image_lib/" + image_str
        self.file = discord.File(f'{path}', filename = "image.png")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if str(payload.emoji) == '\U0001fac0' and payload.user_id == image_lib.user_id:
            message = await self.bot.get_channel(image_lib.channel_id).fetch_message(payload.message_id)
            await message.attachments[0].save(f'A:\Python\Majoneesi\cogs\image_lib\{payload.message_id}.png')
            await self.bot.get_channel(image_lib.log_chid).send('Image has been saved to Image_Lib')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(image_lib(bot))

        

            

