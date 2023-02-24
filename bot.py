
## --- Discord utils
import discord
from discord.ext import commands
## ---

## --- ENV imports
import os
from dotenv import load_dotenv
## ---

## --- APPS
import apps.text.schedule as schedule
import apps.text.randpick as randpick
import apps.audio.yt      as yt
## ---

Ctx_type = discord.ext.commands.Context
CMD_PREFIX = "!"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot( command_prefix=CMD_PREFIX, intents=intents )

@bot.event
async def on_ready() -> None:
    print( "Bot has connected to Discord!" )


## --- TEXT
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

## ---

## --- VOICE
@bot.command( name="join", help="" )
async def join( ctx: Ctx_type, *args: str ) -> None:

    v = ctx.message.author.voice
    if not v:
        await ctx.send( "You are not connected to any voice channel" )
        return

    await ctx.send( f"I am joining {v.channel.name}" )
    await v.channel.connect( )

@bot.command( name="leave", help="" )
async def leave( ctx: Ctx_type, *args: str ) -> None:

    vc = ctx.message.guild.voice_client
    if vc is not None:
        await ctx.send( "Leaving voice channel" )
        await ctx.message.guild.voice_client.disconnect()
    else:
        await ctx.send( "I am not connected to any voice channel" )

@bot.command(name="pause", help="")
async def pause( ctx: Ctx_type ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("I am not playing anything at the moment")
    
@bot.command(name="resume", help="")
async def resume( ctx: Ctx_type ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("I am not playing anything at the moment")

@bot.command(name="stop", help="")
async def stop( ctx: Ctx_type ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("I am not playing anything at the moment")

@bot.command(name="play", help="")
async def play( ctx: Ctx_type, yt_query: str ) -> None:
        voice_client = ctx.message.guild.voice_client
        async with ctx.typing():
            player = await yt.YTDLSource.from_query( yt_query, loop=bot.loop, stream=True )
            voice_client.play( player, after=lambda e: print(f'Player error: {e}') if e else None )

        await ctx.send(f'Now playing: {player.title}')

## ---
bot.run(TOKEN)
