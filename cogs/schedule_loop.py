#✿imports✿
import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime, os.path, os, time, dateutil.parser
from datetime import timedelta
from dateutil import tz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from prettytable import PrettyTable


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Schedule_loopCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.schedule_loop.start()
          
    #✿Adding new loop✿
    @tasks.loop(time=datetime.time(hour=15, minute=58))
    async def schedule_loop(self):
        #✿Linking to Google API✿
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            service = build('calendar','v3',credentials=creds)
        #✿Fetching calendar info✿
            now = datetime.datetime.now().isoformat() + 'Z'
            events_results = service.events().list(calendarId='primary', timeMin=now, maxResults=100, singleEvents=True, orderBy='startTime').execute()
            events = events_results.get('items', [])

        #✿---✿---✿---✿---✿---✿---✿
        #✿Configurations✿
            channel_id = 1031608452084146207
            unix_tz = 28800
            message_id = 1037070041553850440
            update_message_id = 1037388486191349830
        #✿---✿---✿---✿---✿---✿---✿

            if not events:
                await self.bot.get_channel(channel_id).send(f'Nothing UwU')
                return
        
        #✿Set up compilation list✿ 
            my_list_time_show = ""
            my_list_what = ""
            my_list = ""
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                time_converted = time.mktime(dateutil.parser.isoparse(start).timetuple())
                time_converted_show = dateutil.parser.isoparse(start) + timedelta(hours=8)
                my_list += ' ♡ <t:' + str(int(time_converted)+unix_tz) + ':R>  ♡  ' + str(event['summary']) + os.linesep
                my_list_time_show += str(time_converted_show.strftime("%d %b"))+" ♡ "+str(time_converted_show.strftime("%I:%M %p")) +','
                my_list_what += str(event['summary']) +','
            
        #✿Set up table✿ 
            x = PrettyTable()
            x.add_column(" ♡ When ♡ ", my_list_time_show.split(","))
            x.add_column(" ♡ What ♡ ", my_list_what.split(","))
            x.align = "c"
            
        #✿Set up embed✿ 
            embed = discord.Embed(title='Mayo',description='What mayo doing?',color=0xfedbff,timestamp=datetime.datetime.now())
            embed.set_image(url="https://files.yande.re/jpeg/0ff5f6d4f8afe0d0deddbf17c2b58aa6/yande.re%201033861%20cleavage%20halloween%20kano_hito%20pointy_ears%20thighhighs%20wings.jpg")
            embed.add_field(name='₊˚ ✧ ‿︵‿୨୧‿︵ ✧ List ✧ ︵‿୨୧‿︵‿ ✧ ₊˚',value=my_list, inline=False)
            embed.add_field(name='₊˚ ✧ ︵‿୨୧‿︵ ✧ Schedule ✧ ︵‿୨୧‿︵ ✧ ₊˚',value='```\n'+str(x)+'```')
            embed.set_footer(text='(´• ᴗ •`✿)')
            
        #✿Set up embed edit in specific channel✿ 
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            await message.edit(embed=embed)

        #✿Set up last update message✿
            converted_now = time.mktime(datetime.datetime.now().timetuple())
            update_message = await channel.fetch_message(update_message_id)
            await update_message.edit(content=' ♡ Last auto-updated <t:' + str(int(converted_now)) + ':R>  ♡  ')

        except HttpError as error:
                await self.bot.get_channel(channel_id).send(f'Error UwU')

    @schedule_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Schedule_loopCog(bot))