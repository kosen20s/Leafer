import discord
import os
import sqlite3

client = discord.Client()

async def send(channel,*args, **kwargs): return await channel.send(*args, **kwargs)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "草":
        user_name = str(message.author.id)
        img_name = "./images/" + user_name + ".png"
        await message.channel.send(file=discord.File(img_name))
    if message.content == "grass":
        user_name = str(message.author.id)
        img_name = "./images/" + user_name + ".png"
        await message.channel.send(file=discord.File(img_name))
        
if __name__ == "__main__":
    client.run(os.environ['LEAF_TOKEN'])