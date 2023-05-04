# bot.py
from dotenv import load_dotenv
from discord.ext import tasks, commands
import discord
import os
from datetime import datetime, timedelta
import pandas as pd


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')



class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        self.meeting_notification.start()

    async def on_message(self, message):
        if message.author == client.user:
            return
        print(message.content)
        if message.content.startswith('!meet'):
            try:
                meet = message.content.split(',')
                host = message.author.id
                time = meet[1].strip()
                subject = meet[2].strip()
                members = meet[3]
                members = members.split('-')
                members = map(lambda x:x.strip().replace('<@', '').replace('>', ''), members)
                meetings = pd.DataFrame({
                    "time": time,
                    "subject": subject,
                    "member": members,
                    "host": host,
                    "sent": False
                })
                print(meetings)
                hdr = False  if os.path.isfile('meetings.csv') else True
                meetings.to_csv('meetings.csv', encoding='utf-8',mode='a+', index=False, header=hdr)
                await message.channel.send("meeting saved")
            except:
                await message.channel.send("Command form is wrong,\n `!meeting, time, subject, [members]`")
    @tasks.loop(seconds=5.0)
    async def meeting_notification(self):
        meetings = pd.read_csv('meetings.csv')
        for index, meeting in meetings.iterrows():
            meeting_time = datetime.strptime(meeting['time'], '%H:%M')
            diff = datetime.now() - meeting_time
            print(diff)
            print(timedelta(minutes=10))
            if meeting['sent'] == False and diff < timedelta(minutes=10):
                print('Hi')
                member = client.get_user(meeting['member'])
                print(member)
                await self.send_dm(member=member, content="hello it is working !!!")
                meetings.loc[index, "sent"] = True
                meetings.to_csv('meetings.csv', index=False)

    async def send_dm(ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await channel.send(content)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = CustomClient(intents=intents)
client.run(TOKEN)