from discord.ext import tasks

import discord
import os
from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.userID = int(os.getenv('USER_ID'))
        self.members = None
        self.target = None
        self.channel = None
        self.current_song = ""

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        self.members = self.get_all_members()

        for member in self.members:
            print(f"Target: {member.display_name}")
            if member.id == self.userID:
                self.target = member

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        print(self.target.name)
        

    @tasks.loop(seconds=1)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(int(os.getenv('CHANNEL_ID')))  # channel ID goes here
        if isinstance(self.target.activity, discord.Spotify):
            if self.target.activity.artist != self.current_song:
                await channel.send(f"{self.target.mention} imagine listening to {self.target.activity.artist} cringe")
                self.current_song = self.target.activity.artist

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.all())
client.run(os.getenv('TOKEN'))