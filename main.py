import discord

TOKEN = "MTUwNjYwMDIxNTgzNzE0NzE2Nw.G7jpPl.DV0g-vQHnc5Q_EbnJAobcWk10ka3BgM3F8nLzU"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"SUCCESS! Logged in as {client.user}")
    await client.close()

client.run(TOKEN)
