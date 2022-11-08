import os
import discord
from discord import app_commands, Attachment
from discord.ext import commands
import random
import datetime
from PIL import Image

class image_lib(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.path = f'{os.getcwd()}{self.bot.config["image_lib"]["path"]}'
        self.file = discord.File(f'{self.path}/{random.choice (os.listdir(self.path))}', filename = "image.png")
        
    async def image_rand(self):
        list = os.listdir(self.path)
        image_str = random.choice(list)
        path_i = f'{self.path}/' + image_str
        self.file = discord.File(f'{path_i}', filename = "image.png")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if str(payload.emoji) == '\U0001fac0' and payload.user_id == self.bot.config["user_id"]["owner"]:
            message = await self.bot.get_channel(self.bot.config["image_lib"]["channel_id"]).fetch_message(payload.message_id)
            await message.attachments[0].save(f'{self.path}/{payload.message_id}.png')
            await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send('Image has been saved to Image_Lib')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(image_lib(bot))

        

            

