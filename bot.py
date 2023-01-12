
## --- ENV imports
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
## ---

## --- APPS
import schedule
import randpick
## ---


Ctx_type = discord.ext.commands.Context
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


@bot.command( name="when", help=schedule.HELP_MSG )
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

@bot.command( name="pick", help=randpick.HELP_MSG )
async def picker( ctx: Ctx_type, *args: str ) -> None:

    if len( args ) == 0:
        await ctx.send( randpick.EMPTY_ERR )
        return

    picked = randpick.pick( list( args ) )
    await ctx.send( picked )

bot.run(TOKEN)
