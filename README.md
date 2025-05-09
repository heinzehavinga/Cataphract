This will probably end up number of Docker containers.  Right now it's just a bunch
of loose apps.

# Cataphract

## Installation
We should have the Django bot create an AUTH url after you set up an app.
Than use that url to invite the bot to the server.
Than put the discord token in de env variables for the docker compose
Put in a username and password for the Django superuser
Put in a username and password for the Discord bot user

## Django
An automation suite for running a game of Cataphract,
connects to PostGRES database


### Enviroment varaibles for cataphracts
Put a .env file in the cataphracts in dir
DB_NAME = "Name of your database"
DB_USER = "database user"
DB_PASSWORD = "database password"
DB_HOST = "ip of database"
DB_PORT = "database port"


## Discord
Discord bot, will make API call to the Django docker.

https://discordpy.readthedocs.io/en/latest/discord.html

https://discord.com/developers/applications

### Enviroment varaibles for cataphracts
DISCORD_TOKEN


## Map
Will be put into the Django installation?