import os
from dotenv import load_dotenv, dotenv_values 
import discord
from discord.ext import tasks
import io
import requests
load_dotenv() 
import time

django_url = os.getenv('DJANGO_URL')
django_port = os.getenv('DJANGO_PORT')

def format_army_sheet(json):
    message = ""
    if "commander" in json.keys():
        message += f'**Commander: {json["commander"]} (age: {json["age"]})** \n'
    message += f'{json["army_overview"]} \n' 
    message += '\n'
    message += f'Morale {int(json["morale"])} \n'
    message += '\n'
    message += f'Supplies {json["supplies"]}/{json["capacity"]}\n'
    message += f'     Uses {json["supplies_per_day"]} supplies per day\n'
    message += '\n'
    message += f'Detachments:\n'
    for detachment in json["detachments"]:
        message += f'{detachment}\n'
    
    return message

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

        
        #TODO: How would we undo a tick?
        if '/tick' in message.content.lower():
            await self.update_world()
            await message.channel.send('Setting game forward one tick')

        if '/listcommander' in message.content.lower():
            r = requests.get(f'http://{django_url}:{django_port}/cataphract/api/commanders/', auth=(os.getenv('API_USER'), os.getenv('API_PASSWORD')))
            commanders = r.json()
            commander_list_message =  f"Of course {message.author.mention}, Here is a list of all commanders in the game:\n"
            
            for commander in commanders['results']:
                commander_list_message += f"{commander['name']}\n"
            
            await message.channel.send(commander_list_message)

        if '/moralecheck' in message.content.lower():
            r = requests.get(f'http://{django_url}:{django_port}/cataphract/moralecheck/{message.author.id}', auth=(os.getenv('API_USER'), os.getenv('API_PASSWORD')))
            response = r.json()
            morale_outcome =  f"Hey {message.author.mention}, Here is the result of your morale check:\n"
            
            morale_outcome += response['outcome']
            
            await message.channel.send(morale_outcome)

        if '/armysheet' in message.content.lower():
            r = requests.get(f'http://{django_url}:{django_port}/cataphract/commandersheet/{message.author.id}', auth=(os.getenv('API_USER'), os.getenv('API_PASSWORD')))
            sheet = r.json()
            sheet_message = format_army_sheet(sheet)
            
            await message.channel.send(sheet_message)

        if '/calculaterecruit' in message.content.lower():
            r = requests.get(f'http://{django_url}:{django_port}/cataphract/calculaterecruit/{message.author.id}', auth=(os.getenv('API_USER'), os.getenv('API_PASSWORD')))
            sheet = r.json()
            sheet_message = format_army_sheet(sheet)
                
            await message.channel.send(sheet_message)


        if '/showmap' in message.content.lower():
            r = requests.get(f'http://{django_url}:{django_port}/static/test.png', auth=(os.getenv('API_USER'), os.getenv('API_PASSWORD'))) #This will be a API call to dynamically generate image instead of static file.
            with io.BytesIO() as image_binary:
                image_binary.write(r.content)
                image_binary.seek(0)
                await message.channel.send('Here is your current map', file=discord.File(fp=image_binary, filename='map.png'))


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            ##Add it to the queue of availible players, maybe put in a general news chat.
            await guild.system_channel.send(to_send)


    #https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py < Recurring tasks, this will be our main cron loop
    async def setup_hook(self) -> None:
        self.update_world.start()

    # The idea right now is to have a tick last four hours 
    # This loop Should be changed to specific times, like this https://stackoverflow.com/a/77977282
    #Also for our test game we should have a way to manually trigger the next tick.
    # https://www.mikro-mineral.nl/randomgameideas/index.php/Timekeeping
    @tasks.loop(seconds=14400) 
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
        


        ##Create private thread (THIS SNIPPET WORKS, DON'T DELETE)
        # thread = await game_channel.create_thread(name="private test thread", type=None, reason="Used when player are at the same location", invitable=False)
        # for guild in self.guilds:
        #     for role in guild.roles: #This should be done through, guild.get_member and use the id list.
        #         #Than check through all the private_thread to see if the exact combination exsist?
        #         #If it does, set permission correctly again (can this be done per thread?)
        #         #If not create new thread
        #         for member in role.members:
        #             print(role.name, member)
        #             await thread.add_user(member)
        #             time.sleep(4) #Inserted because of ratelimiting
        #For locking threads, just remove persmissions? thread.permissions_for, can be done for role

        
        
        #TODO: make sure bot user has the correct rights (instead of super user) and make user and password an env variable
       

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



if __name__ == '__main__':
    intents = discord.Intents(messages=True, guilds=True, message_content = True, members = True)
    client = CataphractBot(intents=intents)
    
    client.run(os.getenv('DISCORD_TOKEN'))


