import os
from dotenv import load_dotenv, dotenv_values 
import discord
from discord.ext import tasks
load_dotenv() 
import time

#TODO:
# Add a Discord template, that can set up all the things (you can do this to an init function)
# What sort of rights are minimally needed for bot (right now admin, which isn't needed)
# During install write a little test script that check if all needed rights are present.

#Create Roles
    # A role for referee
    # A role for player

#Create game channel
    #The Cataphracts channel


#Testing, is private thread really private?

# https://discordtemplates.me/
#Is there such a thing as discord bot templates? Can we autogenerate the Ouath2 token from the bot?!?!
    #Maybe run docker without token and it spits out the link to you, you add it to the server and it gives you a token you need.

#We need a startup script that show you if you've set all your permissions correctly


class CataphractBot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)


    async def on_message(self, message): #Little function to test if bot if working, just to make sure
        
        print(message.author.name)
        print(message.author.mutual_guilds) #Doesn't work, is guild broken?

        if message.author == self.user:
            return

        if message.content == 'Bot, how goes the game?':
            await message.channel.send(f'The game hasn\'t started yet, {message.author.mention}')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            ##Add it to the queue of availible players, maybe put in a general news chat.
            await guild.system_channel.send(to_send)

    #https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py < Recurring tasks, this will be our main cron loop
    async def setup_hook(self) -> None:
        self.update_world.start()

    @tasks.loop(seconds=3600)  # task runs every hour (maybe once every six hours?)
    async def update_world(self):
        print('update world')
        #Make Django Call
            #Get complete member list that have role of 'player', send to Django.
            #Anyone new? Add it to the database
            #Anyone missing? Message a referee that army should be taken over by new commander!

        #Write some settings to a little file, maybe a sqllite or just a json? To prevent this sort of looping
        # game_channel = None
        # for guild in self.guilds: # This will be smarter if the Discord bot sets it self up. (Maybe a Django model?)
        #     for channel in guild.text_channels:
        #         if channel.name == 'cataphract':
        #             game_channel = channel
        #             print(game_channel.id)

        game_channel = self.get_channel(1369341115018510367)



        ##Create private thread
        thread = await game_channel.create_thread(name="private test thread", type=None, reason="Used when player are at the same location", invitable=False)
        for guild in self.guilds:
            for role in guild.roles: #This should be done through, guild.get_member and use the id list.
                #Than check through all the private_thread to see if the exact combination exsist?
                #If it does, set permission correctly again (can this be done per thread?)
                #If not create new thread
                for member in role.members:
                    print(role.name, member)
                    await thread.add_user(member)
                    time.sleep(4) #Inserted because of ratelimiting

            


        #For locking threads, just remove persmissions? thread.permissions_for, can be done for role


        #Get list of tasks Post @everyone (only active player group) the new tick has happend (do we need that?), opening channels, send users their new map, etc.)
        
        #fetch_channel(channel_id, /) #We need a channel for all the private threads?
        #fetch_channel(channel_id, /) #We need a channel for the daily update?

        #Daily report, is this a DM?
        #This is probably also the place, the referees talk to the commander, we need to support multiple referees, so this is probably a thread.

        #Are commaners no longer on the same hex? Close/Archive their thread!
        # active_threads() Get all threads
        # https://discordpy.readthedocs.io/en/latest/api.html#discord.Thread.edit

        #Are several commanders on the same hex? Let's open a challen for them!
        # create_thread https://discordpy.readthedocs.io/en/latest/api.html#discord.TextChannel.create_thread
        # await create_thread(*, name, message=None, auto_archive_duration=..., type=None, reason=None, invitable=True, slowmode_delay=None)
        #Invite user
        #https://discordpy.readthedocs.io/en/latest/api.html#discord.Thread.add_user

        # message = 'tick'
        # await channel.send(message)

    @update_world.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

intents = discord.Intents(messages=True, guilds=True, message_content = True, members = True)
client = CataphractBot(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))


