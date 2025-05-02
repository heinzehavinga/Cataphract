import os
from dotenv import load_dotenv, dotenv_values 
import discord
load_dotenv() 


class CataphractBot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents(messages=True)
intents.message_content = True
client = CataphractBot(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))


#Does the discord bot run the whole thing? Does it make the time call and based on 