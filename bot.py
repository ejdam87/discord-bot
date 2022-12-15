import discord

TOKEN = "MTA1MzAwMzEwODUwODI0MTk2MQ.Gg9ICW.WXmlSNCmSNS_dp8w6f-qFfd_8TO-mg_eMULEKg"

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):

    if message.content == '99!':
        response = random.choice("Hello")
        await message.channel.send(response)

client.run(TOKEN)
