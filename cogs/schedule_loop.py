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
        self.x = []
        self.my_list_time_show = ''
        self.my_list_what = ''
        self.my_list = ''
        self.initial = True
        self.my_list_time_show_s = ''
        self.my_list_what_s = ''
        self.my_list_s = ''
        self.schedule_loop.start() 

    #✿Linking to Google API✿
    async def google(self):
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
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_results = service.events().list(calendarId='primary', timeMin=now, maxResults=100, singleEvents=True, orderBy='startTime').execute()
            events = events_results.get('items', [])
            if not events:
                await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(f'Nothing UwU')
                return
            
        except HttpError as error:
                await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(f'Error UwU')

        #✿Set up compilation list✿ 
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            time_converted = time.mktime(dateutil.parser.isoparse(start).timetuple())
            time_converted_show = dateutil.parser.isoparse(start) + timedelta(hours=8)
            self.my_list += ' ♡ <t:' + str(int(time_converted)+self.bot.config["schedule"]["unix_tz"]) + ':R>  ♡  ' + str(event['summary']) + os.linesep
            self.my_list_time_show += str(time_converted_show.strftime("%d %b"))+" ♡ "+str(time_converted_show.strftime("%I:%M %p")) +','
            self.my_list_what += str(event['summary']) +','
            print(self.my_list)
        
        #✿Set up table✿ 
        self.x = PrettyTable()
        self.x.add_column(" ♡ When ♡ ", self.my_list_time_show.split(","))
        self.x.add_column(" ♡ What ♡ ", self.my_list_what.split(","))
        self.x.align = "c"

    #✿Adding new loop✿
    @tasks.loop(minutes = 15)
    async def schedule_loop(self):
        if self.initial == True:
            image_lib = self.bot.get_cog('image_lib')
            await image_lib.image_rand()
            self.initial = False
            self.my_list_time_show = ''
            self.my_list_what = ''
            self.my_list = ''
            await self.google()
            self.my_list_time_show_s = self.my_list_time_show
            self.my_list_what_s = self.my_list_what
            self.my_list_s = self.my_list
            
            #✿Set up embed✿ 
            embed = discord.Embed(title='Mayo',description='What mayo doing?',color=0xfedbff,timestamp=datetime.datetime.now())
            embed.set_image(url="attachment://image.png")
            embed.add_field(name='₊˚ ✧ ‿︵‿୨୧‿︵ ✧ List ✧ ︵‿୨୧‿︵‿ ✧ ₊˚',value=self.my_list, inline=False)
            embed.add_field(name='₊˚ ✧ ︵‿୨୧‿︵ ✧ Schedule ✧ ︵‿୨୧‿︵ ✧ ₊˚',value='```\n'+str(self.x)+'```')
            embed.set_footer(text='(´• ᴗ •`✿)')
                
            #✿Set up embed edit in specific channel✿ 
            channel = self.bot.get_channel(self.bot.config["schedule"]["channel_id"])
            message = await channel.fetch_message(self.bot.config["schedule"]["schedule_msg"])
            await message.edit(attachments=[image_lib.file], embed=embed)
            print ('Initial schedule updated automatically')
            #✿Set up last update message (log)✿
            await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(content = 'Initial schedule updated automatically')

        elif self.initial == False:
            image_lib = self.bot.get_cog('image_lib')
            await image_lib.image_rand()
            self.my_list_time_show = ''
            self.my_list_what = ''
            self.my_list = ''
            await self.google()
            if self.my_list_s == self.my_list:
                return
            elif self.my_list_s != self.my_list:
                #✿Set up embed✿ 
                embed = discord.Embed(title='Mayo',description='What mayo doing?',color=0xfedbff,timestamp=datetime.datetime.now())
                embed.set_image(url="attachment://image.png")
                embed.add_field(name='₊˚ ✧ ‿︵‿୨୧‿︵ ✧ List ✧ ︵‿୨୧‿︵‿ ✧ ₊˚',value=self.my_list, inline=False)
                embed.add_field(name='₊˚ ✧ ︵‿୨୧‿︵ ✧ Schedule ✧ ︵‿୨୧‿︵ ✧ ₊˚',value='```\n'+str(self.x)+'```')
                embed.set_footer(text='(´• ᴗ •`✿)')
                    
                #✿Set up embed edit in specific channel✿ 
                channel = self.bot.get_channel(self.bot.config["schedule"]["channel_id"])
                message = await channel.fetch_message(self.bot.config["schedule"]["schedule_msg"])
                await message.edit(attachments=[image_lib.file], embed=embed)
                print ('Schedule updated automatically')
                #✿Set up last update message (log)✿
                await self.bot.get_channel(self.bot.config["channel_id"]["log"]).send(content = 'Schedule updated automatically')

                self.my_list_time_show_s = self.my_list_time_show
                self.my_list_what_s = self.my_list_what
                self.my_list_s = self.my_list
        

    @schedule_loop.before_loop
    async def tasks_before_loop(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.schedule_loop.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Schedule_loopCog(bot))