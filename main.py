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
            image_name = grass + ".svg"
            command = COMMAND_BASE.format(url=url) + image_name
            print(command)
            os.system(command)

            file_name = "./images/" + image_name
            converted_file_output = "--output=" + "./images/" + grass + ".png"
            user_id = message.author.id
            subprocess.run(["rsvg-convert", "--format=png",  file_name, converted_file_output])

            converted_file_name = grass + ".png"
            sql = 'insert into grass (username, filename) values (?,?)'
            namelist = (user_id, converted_file_name)
            cursor.execute(sql, namelist)
            connection.commit()
        else:
            await message.channel.send("存在していないuserです\n最初からやり直してください")
        return

    if message.content == '!leaf remove':
        username = str(message.author.id)
        select_sql = 'select * from grass where username=' + username
        print(select_sql)
        cursor.execute(select_sql)
        result = cursor.fetchone()
        img_name = "./images/" + img_name[1]
        rm = "rm " + img_name
        os.system(rm)
        delete_sql = 'delete from grass where username=' + username
        cursor.execute(delete_sql)
        connection.commit()
        await message.channel.send("削除が完了しました")

if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])
