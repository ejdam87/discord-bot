
## --- Discord utils
import discord
from discord.ext import commands
## ---

## --- ENV imports
import os
from dotenv import load_dotenv
## ---

## --- APPS
import apps.text.randpick          as randpick
import apps.text.nameday           as nameday
import apps.audio.yt               as yt
import apps.image.image_generation as imgen
## ---

Context = discord.ext.commands.Context
CMD_PREFIX = "!"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot( command_prefix=CMD_PREFIX, intents=intents )

@bot.event
async def on_ready() -> None:
    print( "Bot has connected to Discord!" )


## --- TEXT
@bot.command( name="pick", help=randpick.HELP_MSG )
async def picker( ctx: Context, *args: str ) -> None:

    if len( args ) == 0:
        await ctx.send( randpick.EMPTY_ERR )
        return

    picked = randpick.pick( list( args ) )
    await ctx.send( picked )

@bot.command( name="nameday", help=nameday.HELP_MSG )
async def picker( ctx: Context, *args: str ) -> None:

    if len( args ) == 0:
        await ctx.send( nameday.get_nameday("sk") )
    elif len( args ) == 1:
        await ctx.send( nameday.get_nameday(args[0]) )
    else:
        if not ( args[1].isnumeric() and args[2].isnumeric() ):
            await ctx.send( "Sefe skus prirodzene cisla zadat plz" )
        else:
            await ctx.send( nameday.get_nameday(args[0], int(args[1]), int(args[2])) )
## ---

## --- AUDIO
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
queue2 = []

@bot.command(name="play", help="Play a song and add it to the queue.")
async def play(ctx: Context, yt_query: str) -> None:
    voice_client = ctx.message.guild.voice_client

    async with ctx.typing():
        player = await yt.YTDLSource.from_query(yt_query, loop=bot.loop, stream=True)

        if voice_client.is_playing():
            queue.append(player)
            queue2.append(yt_query)
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
        queue2.pop(0)

@bot.command(name="pipik", help="Show your pipi size.")
async def pipik(ctx: commands.Context) -> None:
    user_name = ctx.message.author.display_name
    if user_name == 'vilkyway':
        await ctx.send(f"@{user_name} ma pipik o velkosti 6.23 cm (to viem presne).")
    elif user_name == 'Elenka':
        await ctx.send(f"@{user_name} ma pipik enormny, giganticky, OBROVSKY.")
    else:
        from random import uniform
        size = round(uniform(5.00, 30.00), 2)
        await ctx.send(f"@{user_name} ma pipik o velkosti {size} cm.")

@bot.command(name="list", help="Show list of songs")
async def my_list(ctx: Context) -> None:
    print_songs = ""
    for i, song in enumerate(queue2):
        print_songs = print_songs + f"{i + 1}. **{song}**\n"

    print_songs = print_songs if print_songs != "" else "The queue is empty!"
    await ctx.send(print_songs)       
## ---

## --- IMAGE
@bot.command( name="draw", help=imgen.HELP_MSG )
async def drawing( ctx: Context, *args: str ) -> None:
    if len( args ) == 0:
        await ctx.send( imgen.EMPTY_ERR )
        return

    res = imgen.generate( list( args )[0], HUGGINGFACE_TOKEN )
    await ctx.send( file=discord.File(fp=res, filename='image.png') )
## ---

bot.run(TOKEN)
