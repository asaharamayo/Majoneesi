import discord
from discord import app_commands, FFmpegPCMAudio
from discord.ext import commands



class SongCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.bot=client
        
    @commands.command()
    async def akibday(self, ctx):
        if ctx.author.voice is None:
            return
        if ctx.author.voice is not None:
            await ctx.author.voice.channel.connect()
            source = discord.FFmpegPCMAudio('[Mayo] Glow.mp3')
            ctx.voice_client.play(source, after=ctx.author.voice.channel.disconnect())
            print('Playing!')
            await ctx.voice_client.disconnect()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SongCog(bot))