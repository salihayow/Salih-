import discord

TOKEN = "MTUwNjYwMDIxNTgzNzE0NzE2Nw.GoJcMH.Zz056wVQlsgkhU0kmrCkZmRpKhlWq_Ku83u48Y"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ ONLINE: {client.user} is live")
    await client.close()

client.run(TOKEN)
