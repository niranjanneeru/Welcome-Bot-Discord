import discord

from welcome import make_image

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    filename = make_image(member.avatar_url)
    if filename:
        channel = client.get_channel(774694307919429706)
        print("Sending Image...")
        await channel.send(file=discord.File(filename))
        await channel.send(f'<@{member.id}>')


client.run("")
