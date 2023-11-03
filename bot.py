
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
import apps.text.shop     as shop
import apps.audio.yt      as yt
## ---

Context = discord.ext.commands.Context
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
@bot.command( name="shop", help="" )
async def shoping( ctx: Context, *args: str ) -> None:
    
    response = "Query did not match any command!"

    if len( args ) >= 2 and args[ 0 ] == "add":
        for arg in args[ 1: ]:
            shop.push( arg )
        response = "Successfully added!"

    elif len( args ) == 2 and args[ 0 ] == "remove":
        if args[ 1 ].isdecimal():
            shop.remove_nth( int( args[ 1 ] ) )
            response = "Successfully removed!"
        else:
            response = "Invalid number provided!"

    elif len( args ) == 1 and args[ 0 ] == "reset":
        shop.reset()
        response = "Successfully reset!"

    elif len( args ) == 1 and args[ 0 ] == "show":
        lst = shop.fetch()
        response = "empty" if len( lst ) == 0 else "\n".join( lst )

    await ctx.send( response )

@bot.command( name="when", help=schedule.HELP_MSG )
async def time_table( ctx: Context, *args: str ) -> None:

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
async def picker( ctx: Context, *args: str ) -> None:

    if len( args ) == 0:
        await ctx.send( randpick.EMPTY_ERR )
        return

    picked = randpick.pick( list( args ) )
    await ctx.send( picked )

## ---

## --- VOICE
@bot.command( name="join", help="" )
async def join( ctx: Context, *args: str ) -> None:

    v = ctx.message.author.voice
    if not v:
        await ctx.send( "You are not connected to any voice channel" )
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is not None:
        await ctx.send( "I am already connected to a voice channel" )
        return

    await ctx.send( f"I am joining {v.channel.name}" )
    await v.channel.connect( )

@bot.command( name="leave", help="" )
async def leave( ctx: Context, *args: str ) -> None:

    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        await ctx.send( "Leaving voice channel" )
        await voice_client.disconnect()
    else:
        await ctx.send( "I am not connected to any voice channel" )

@bot.command( name="pause", help="" )
async def pause( ctx: Context ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send( "I am not playing anything at the moment" )
    
@bot.command( name="resume", help="" )
async def resume( ctx: Context ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send( "I am not playing anything at the moment" )

@bot.command( name="stop", help="" )
async def stop( ctx: Context ) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send( "I am not playing anything at the moment" )

queue = []

@bot.command(name="play", help="Play a song and add it to the queue.")
async def play(ctx: Context, yt_query: str) -> None:
    voice_client = ctx.message.guild.voice_client

    async with ctx.typing():
        player = await yt.YTDLSource.from_query(yt_query, loop=bot.loop, stream=True)

        if voice_client.is_playing():
            queue.append(player)
            await ctx.send(f"**Added to queue**: {player.title}")
        else:
            voice_client.play(player, after=lambda e: on_song_end(e))

            await ctx.send(f"**Playing now**: {player.title}")

@bot.command(name="skip", help="Skip the current song.")
async def skip(ctx: Context) -> None:
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send( "Mirko, sa co chces skipovat ked sa nic nehra" )
        

def on_song_end(error):
    if error:
        print(f'Error in song playback: {error}')

    if queue:
        voice_client = bot.voice_clients[0]
        player = queue.pop(0)
        voice_client.play(player, after=lambda e: on_song_end(e))
        
## ---
bot.run(TOKEN)
