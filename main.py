# -*- coding: utf-8 -*-
import asyncio
import discord
import subprocess
import os
import requests
from urllib.parse import urljoin
import sqlite3
client = discord.Client()
conn = sqlite3.connect('grass.db')
c = conn.cursor()

async def send(channel,*args, **kwargs): return await channel.send(*args, **kwargs)
 
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!leaf set':
        await message.channel.send("設定します ユーザー名を続けて入力して下さい")

    def check(command):
        return command.author == message.author
    cc = await client.wait_for("message", check=check)
    grass = cc.content
    baseurl = "https://github.com"
    url = urljoin(baseurl, grass)
    command = '/usr/bin/curl {url} | awk \'/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/\' | sed -e \'s/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/\' > test.svg'
    command = command.format(url=url)
    print(command)
    grass_image = os.system(command)
    grass_image_name = grass + ".svg"
    grass_image = str(grass_image)
    f = open(grass_image_name, "w")
    f.write(grass_image)
    f.close()
    grass_convert_fname = "--output=" + grass + ".png"
    subprocess.run(["rsvg-convert", "--format=png",  grass_image_name, grass_convert_fname])
    uname = message.author.id
    sql = 'insert into grass (username, filename) values (?,?)'
    namelist = (uname, grass_convert_fname)
    c.execute(sql, namelist)
    conn.commit()
    if message.content == '草':
        user_name = message.author.id
        select_sql = 'select * from grass where username='
        username = ('{user_name}')
        select_sql = select_sql + username
        c.execute(select_sql)
        result=c.fetchone()
        
        


if __name__ == "__main__":
    client.run()