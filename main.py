import shutil

import cv2
import discord
import requests

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    r = requests.get(member.avatar_url, stream=True,
                     headers={'User-agent': 'Mozilla/5.0'})
    print("Downloading Image")
    if r.status_code == 200:
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    try:
        img = cv2.imread('img.png')
        img = cv2.resize(img, (130, 130), interpolation=cv2.INTER_AREA)
        h, w = 130, 130  # img.shape

        # load background image as grayscale

        back = cv2.imread('background.png')
        hh, ww = 480, 720  # back.shape

        # compute xoff and yoff for placement of upper left corner of resized image
        yoff = round((hh - h - 140) / 2)
        xoff = round((ww - w) / 2)

        # use numpy indexing to place the resized image in the center of background image
        result = back.copy()
        result[yoff:yoff + h, xoff:xoff + w] = img

        # save resulting centered image
        filename = 'welcome.png'
        cv2.imwrite(filename, result)
        print("Image Created")
    except:
        filename = None

    if filename:
        channel = client.get_channel(774694307919429706)
        print("Sending Image...")
        await channel.send(file=discord.File(filename))
        await channel.send(f'<@{member.id}>')


client.run("")
