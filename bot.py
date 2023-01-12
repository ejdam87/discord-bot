
## --- ENV imports
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
## ---

## --- APPS
import schedule
## ---


Ctx_type = discord.ext.commands.Context

HELP_MSG = "To find out when we playing type: '!when'"
CMD_PREFIX = "!"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot( command_prefix=CMD_PREFIX, intents=intents )

@bot.event
async def on_ready() -> None:
    print( "Bot has connected to Discord!" )


@bot.command( name="when", help=HELP_MSG )
async def time_table( ctx: Ctx_type, *args: str ) -> None:

    if len( args ) == 2 and args[ 0 ]  == "get":
        day = args[ 1 ]
        when = schedule.get_playtime( day )
        response = f"Playtime for {day}: {when}"

    elif len( args ) == 3 and args[ 0 ] == "set":
        day = args[ 1 ]
        when = args[ 2 ]
        schedule.set_playtime( day, when )
        response = f"Playtime for {day} was set for: {when}"

    else:
        response = schedule.ERROR_MSG

    await ctx.send( response )

bot.run(TOKEN)
