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
    grass_image_name = grass + ".svg"
    command = '/usr/bin/curl {url} | awk \'/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/\' | sed -e \'s/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/\''
    command = command + ">" + grass_image_name
    command = command.format(url=url)
    print(command)
    grass_image = os.system(command)
    grass_convert_fname = "--output=" + grass + ".png"
    subprocess.run(["rsvg-convert", "--format=png",  grass_image_name, grass_convert_fname])
    uname = message.author.id
    grass_convert_fname = grass + ".png"
    sql = 'insert into grass (username, filename) values (?,?)'
    namelist = (uname, grass_convert_fname)
    c.execute(sql, namelist)
    conn.commit()
    # if message.content == '草':
    #     user_name = message.author.id
    #     select_sql = 'select * from grass where username='
    #     username = ('{user_name}').format(user_name=user_name)
    #     select_sql = select_sql + username
    #     print(select_sql)
    #     c.execute(select_sql)
    #     result=c.fetchone()
    #     # print(result)
    #     # DBから出てきたデータは16桁のIDが最初にあるので17文字目まで切り捨てることができる
    #     # m = result.decode()
    #     # print(result)
    #     img_name = result[1]
    #     await message.channel.send(file=discord.File(img_name))
    #     print(result[1])


if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])