import discord
import os
import sqlite3

client = discord.Client()
conn = sqlite3.connect('grass.db')
c = conn.cursor()

async def send(channel,*args, **kwargs): return await channel.send(*args, **kwargs)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "草":
        user_name = message.author.id
        select_sql = 'select * from grass where username='
        username = ('{user_name}').format(user_name=user_name)
        select_sql = select_sql + username
        print(select_sql)
        c.execute(select_sql)
        result = c.fetchone()
        img_name = result[1]
        img_name = "./images/" + img_name
        await message.channel.send(file=discord.File(img_name))
    if message.content == "grass":
        user_name = message.author.id
        select_sql = 'select * from grass where username='
        username = ('{user_name}').format(user_name=user_name)
        select_sql = select_sql + username
        print(select_sql)
        c.execute(select_sql)
        result = c.fetchone()
        img_name = result[1]
        img_name = "./images/" + img_name
        img_name_n = img_name.replace(".png","")
        await message.channel.send(img_name_n)
        await message.channel.send(file=discord.File(img_name))
        
if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])