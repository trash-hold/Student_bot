from discord.ext import commands
from discord import app_commands 
import discord as d
import asyncio
import aiohttp
import io
import random
import requests
from bs4 import BeautifulSoup
import random

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

class Podstawowe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @app_commands.command()
    async def student(self, interaction: d.Interaction):
        '''
        Odpowiedź na odwieczne filozoficzne pytanie o esencję ludzkiego bytu - kim jestem?
        '''  
        await interaction.message.reply('debil')

    @app_commands.command()
    async def debil(self, interaction: d.Interaction):
            '''
            Wstąp na drogę oświecenia
            '''
            response = requests.get(url = 'https://pl.wikipedia.org/wiki/Special:Random')

            if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.find(id='firstHeading')
                    await interaction.response.send_message(f"Dla własnego dobra przeczytaj o: {title.string} \n {str(response.url)}")
            else:
                    await interaction.response.send_message("Once a student, always a debil")
    

    @app_commands.command()
    @app_commands.checks.has_permissions(administrator = True)
    async def papiesh(self, interaction: d.Interaction):
        '''
        Student bot ma dla Ciebie miłą niespodziankę
        '''
        #await interaction.response.send_message("debil")
        url = get_url()
        channel = self.bot.get_channel(interaction.channel_id)
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                        if resp.status != 200:
                                return await channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await interaction.response.send_message(file=d.File(data,'papa.png'))



async def setup(bot):
    await bot.add_cog(Podstawowe(bot))