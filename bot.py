import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

import when

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
async def time_table( ctx ) -> None:
    response = f"Today we're playing at: {when.get_time_today()}"
    await ctx.send( response )

bot.run(TOKEN)
