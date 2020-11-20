import io

import discord
import requests
from PIL import Image

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    r = requests.get(member.avatar_url, stream=True,
                     headers={'User-agent': 'Mozilla/5.0'})
    print("Downloading Image")
    try:
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            img = img.resize((130, 130))
            img = img.convert("RGBA")
            h, w = 130, 130  # img.shape

            # load background image as grayscale

            back = Image.open('background.png')
            hh, ww = 480, 720  # back.shape
            back = back.resize((ww, hh))

            # compute xoff and yoff for placement of upper left corner of resized image
            yoff = round((hh - h - 140) / 2)
            xoff = round((ww - w) / 2)

            # use numpy indexing to place the resized image in the center of background image
            result = back.copy()
            result.paste(img,box=(xoff,yoff,xoff+w,yoff+h),mask=img)
            # result[yoff:yoff + h, xoff:xoff + w] = img

            # save resulting centered image
            filename = 'welcome.png'
            result.convert(back.mode).save(filename)
            print("Image Created")
    except Exception as e:
        print(e)
        filename = None

    if filename:
        channel = client.get_channel(774694307919429706)
        print("Sending Image...")
        await channel.send(file=discord.File(filename))
        await channel.send(f'<@{member.id}>')


client.run("")
