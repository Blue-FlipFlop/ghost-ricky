# bot.py
import os
import asyncio
import time

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(client.guilds)
    await client.change_presence(activity=discord.Game(name='~ghost_ricky info'))

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    if message.author.bot:
        return
    print("received something")
    content = message.content
    ids = {"IB": 1,
           "Rickys Server": 726167509249687573
           }
    if content.startswith("~ghost_ricky"):
        if "info" in content:
            await message.author.send(  "```**Info** - Sends info box\n" +
                                        "~ghost_ricky info\n\n" +
                                        "**Delay** - Sends Message after Given Seconds\n" +
                                        "~ghost_ricky delay server=\"\" channel=\"\" days=\"\" hours=\"\" minutes=\"\" seconds=\"\" message=\"\"\n\n" +
                                        "Fields default to 0\n" +
                                        "Example: ~ghost_ricky delay server=\"IB\" channel=\"lounge\" seconds=5 message=\"A\"```")
        #elif "delay" in content:
        else:
            try:
                newchannel = channel
                if "channel=" in content and "server=" not in content:
                    i = content.index("channel=")
                    newchanneltxt = content[(i + 9):(content.index("\"", i + 10))]
                    newchannel = discord.utils.get(message.guild.text_channels, name=newchanneltxt)
                if "channel=" and "server=" in content:
                    i = content.index("channel=")
                    j = content.index("server=")
                    newchanneltxt = content[(i + 9):(content.index("\"", i + 10))]
                    server = content[(j + 8):(content.index("\"", j + 9))]
                    if server not in ids:
                        await channel.send("can't find server")
                        print("not in server")
                        return
                    newchannel = discord.utils.get(client.get_guild(ids[server]).text_channels, name=newchanneltxt)
                delay = 0
                if "days=" in content:
                    i = content.index("hours=")
                    delay += 86400 * int(content[(i + 6):(content.index("\"", i + 7))])
                if "hours=" in content:
                    i = content.index("hours=")
                    delay += 3600 * int(content[(i + 7):(content.index("\"", i + 8))])
                if "minutes=" in content:
                    i = content.index("minutes=")
                    delay += 60 * int(content[(i + 9):(content.index("\"", i + 10))])
                if "seconds=" in content:
                    i = content.index("seconds=")
                    delay += 1 * int(content[(i + 9):(content.index("\"", i + 10))])
                if "message=" in content:
                    i = content.index("message=")
                    message = content[(i + 9):(content.index("\"", i + 10))]
                else:
                    return
                if delay < 0:
                    await channel.send("don't do that")
                await timed_print(delay, message, newchannel)
            except:
                await channel.send("something's wrong")


async def timed_print(seconds, content, channel):
    print("printing", content, "in", seconds, "seconds")
    await asyncio.sleep(seconds)
    await channel.send(content)


client.run(TOKEN)
