import discord
from discord import app_commands
from discord.ext import commands
import datetime, os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class ScheduleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
    
    #✿Configurations✿
    
    
    #✿Adding new command ",,Update"✿
    @commands.command()
    async def update(self, ctx):
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
            now = datetime.datetime.now().isoformat() + 'Z'
            events_results = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
            events = events_results.get('items', [])

            channel_id = 1031608452084146207

            if not events:
                await self.bot.get_channel(channel_id).send(f'Nothing UwU')
                return

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                await self.bot.get_channel(channel_id).send(start[0:19] + event['summary'])

        except HttpError as error:
                await self.bot.get_channel(channel_id).send(f'Error UwU')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ScheduleCog(bot))