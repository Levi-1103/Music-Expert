from discord.ext import tasks

import discord
import os
from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

        self.target_name = ""
        self.members = None
        self.target = None
        self.current_song = ""

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        self.members = self.get_all_members()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            if message.content.startswith('target'):
                channel = message.channel
                await channel.send('Enter the target Name')

                # def check(m):
                #     print("CHECK")
                #     return # m.channel == channel and (len(m.content) == 17 or len(m.content) == 18)

                msg = await client.wait_for('message')

                for member in self.members:
                    if member.name == msg.content:
                        self.target_name = member.name
                        self.target = member

                await channel.send(f'Target Acquired {self.target.name}')

    @tasks.loop(seconds=1)
    async def my_background_task(self):
        if self.target is None:
            print("NO TARGET")
            return
        else:
            # print(self.target.activities)
            channel = self.get_channel(int(os.getenv('CHANNEL_ID')))
            
            if isinstance(self.target.activities[1], discord.Spotify):
                activity = self.target.activities[1]
                if activity.artist != self.current_song:
                    await channel.send(f"{self.target.mention} imagine listening to {activity.artist} cringe")
                    self.current_song = activity.artist

        

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()


client = MyClient(intents=discord.Intents.all())
client.run(os.getenv('TOKEN'))