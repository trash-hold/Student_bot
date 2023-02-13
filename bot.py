import os 
import io
import aiohttp
import discord as d
import random
import math as m

#web scrapping
import requests
from bs4 import BeautifulSoup

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = d.Intents.all()
client = d.Client(intents=intents)

bot = commands.Bot(intents = intents, command_prefix = '!')


def get_url(predifned = False):
        url = None
        if predifned:
                print("ugabuga")
        else:
                url_hardcode= [
                        'https://bi.im-g.pl/im/9b/1b/19/z26328731AMP,Papiez-z-glazem--Nowa-instalacja-Jerzego-Kaliny-na.jpg',
                        'https://preview.redd.it/hk7pt3fizhq51.jpg?auto=webp&s=93b2ba7f951a2dd383ec999624d2075fd14e1332',
                        'https://scontent-waw1-1.xx.fbcdn.net/v/t1.6435-9/120930804_3462690147099440_5661359718683705803_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=730e14&_nc_ohc=1RGJxDO6LC4AX_swExn&_nc_oc=AQnineipb42Vsoi6VmJqzQrOHIElmFAtI8JbhSshSx3h88DYwH8t1S4kyh46O1kAG2kqAo5mv6hppsYwCqHVUjZJ&_nc_ht=scontent-waw1-1.xx&oh=00_AfAWzbXHi-y4BJmVeIwPD6-Iq7ajm4_lTFxClY--ThN6Bg&oe=6400E38C',
                        'https://wykop.pl/cdn/c3201142/comment_tQ0qfDHRtasVdr5G7LvTeX4BfMX6yNWV,w400.jpg',
                        'https://i.redd.it/cgrp3tll5r151.jpg',
                ]
                n = random.randint(0, len(url_hardcode)-1)
                url = url_hardcode[n]
        return url

@bot.listen('on_message')
async def background(ctx):
        cheers = ('jeb', 'pierdol', 'chuj')
        content = ctx.content.lower()
        for i in cheers:
                if i in content:
                        await ctx.add_reaction('🍻')


@bot.command(name='papiesh')
async def test(ctx):
        #await ctx.send("debil")
        url = get_url()
        channel = bot.get_channel(ctx.channel.id)
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                        if resp.status != 200:
                                return await channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await channel.send(file=d.File(data,'papa.png'))

#@bot.command(name = 'tmp', help = 'Student debil tworzy kanał, w wyniku nadmiernej alkoholizacji zapomina wszystkie wysłane tam wiadomości w przeciągu ostatnich 30 minut')


@bot.command(name = 'student', help = 'Odpowiedź na odwieczne filozoficzne pytanie o esencję ludzkiego bytu - kim jestem?')
async def student(ctx):
        await ctx.reply('debil')

@bot.command(name = 'debil', help = 'Wstąp na drogę oświecenia')
async def debil(ctx):
        response = requests.get(url = 'https://pl.wikipedia.org/wiki/Special:Random')

        if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find(id='firstHeading')
                await ctx.send(f"Dla własnego dobra przeczytaj o: {title.string} \n {str(response.url)}")
        else:
                await ctx.send("Once a student, always a debil")


@bot.command(name = 'clear')
async def clear_channel(ctx):
        if ctx.message.author.guild_permissions.administrator:
                await ctx.channel.purge()
        else:
                await ctx.channel.send('Niestety nie możesz siać masowej destrukcji :/')
                


bot.run(TOKEN)