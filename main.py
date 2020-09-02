# -*- coding: utf-8 -*-
import asyncio
import discord
import subprocess
import os
import requests
from urllib.parse import urljoin
import sqlite3
client = discord.Client()
connection = sqlite3.connect('grass.db')
cursor = connection.cursor()
BASEURL = "https://github.com"

COMMAND_BASE = "/usr/bin/curl '{url}' | awk '/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/' | sed -e 's/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/'>./images/"

async def send(channel,*args, **kwargs): return await channel.send(*args, **kwargs)
 
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!leaf set':
        await message.channel.send("設定します ユーザー名を続けて入力して下さい")

        def check(command):
            return command.author == message.author

        reply = await client.wait_for("message", check=check)

        grass = reply.content.lower()

        url = urljoin(BASEURL, grass)
        req = requests.get(url)
        print(url)
        print(req)
        if req.status_code == requests.codes.ok:
            grass_image_name = grass + ".svg"
            command = COMMAND_BASE.format(url=url) + grass_image_name
            print(command)
            grass_image = os.system(command)
            grass_image_name = "./images/" + grass_image_name
            grass_convert_fname = "--output=" + "./images/" +grass + ".png"
            subprocess.run(["rsvg-convert", "--format=png",  grass_image_name, grass_convert_fname])
            uname = message.author.id
            grass_convert_fname = grass + ".png"
            sql = 'insert into grass (username, filename) values (?,?)'
            namelist = (uname, grass_convert_fname)
            cursor.execute(sql, namelist)
            connection.commit()
        else:
            await message.channel.send("存在していないuserです\n最初からやり直してください")
        return

    if message.content == '!leaf remove':
        user_name = message.author.id
        select_sql = 'select * from grass where username='
        select_sql = str(select_sql)
        user_name = str(user_name)
        username = ('{user_name}').format(user_name=user_name)
        select_sql = select_sql + user_name
        print(select_sql)
        cursor.execute(select_sql)
        result = cursor.fetchone()
        img_name = result[1]
        img_name = "./images/" + img_name
        rm = "rm " + img_name
        os.system(rm)
        sql = 'delete from grass where username=' + username
        cursor.execute(sql)
        connection.commit()
        await message.channel.send("削除が完了しました")

if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])
