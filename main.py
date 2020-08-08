# -*- coding: utf-8 -*-
import asyncio
import discord
import subprocess
import os
import requests
from urllib.parse import urljoin

server_id = 665189315877535753

server_id = int(server_id)

client = discord.Client()

async def send(channel,*args, **kwargs): return await channel.send(*args, **kwargs)
 
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!leaf set':
        await message.channel.send("設定します ユーザー名を続けて入力して下さい")

    def check(command):
        return command.author == message.author
    c = await client.wait_for("message", check=check)
    grass = c.content
    baseurl = "https://github.com"
    url = urljoin(baseurl, grass)
    grass_image = subprocess.check_output(['curl', url, '|', "awk", "'/<svg.+class="js-calendar-graph-svg"/,/svg>/'", "|", 'sed', '-e', 's/<svg/<svg xmlns="http:\/\/www.w3.org\/2000\/svg"/'])
    grass_image_name = grass + ".svg"
    f = open(grass_image_name, "w")
    f.write(grass_image)
    f.close()
    if message.content == '草':


if __name__ == "__main__":
    client.run(os.environ['MARK1_TOKEN'])