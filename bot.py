import os 
import asyncio
import discord as d

import math as m

import os 

#web scrapping
import requests
from bs4 import BeautifulSoup

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = d.Intents.all()
client = d.Client(intents=intents)

bot = commands.Bot(intents = intents, command_prefix = '/')
tree = app_commands.CommandTree(client)

'''class Test(app_commands.Group):

        @app_commands.command()
        @app_commands.describe(test = 'Test of sync')
        async def test(self, interaction: d.Interaction):
                await interaction.response.send_message('I guess it worked!')
'''

@bot.tree.command()
async def test(interaction: d.Interaction):
        await interaction.response.send_message('FUCK OFF')

@bot.tree.command()
async def hihi(interaction: d.Interaction):
        await interaction.response.send_message('MICHEAL?')

@bot.command(name = 'sync')
@commands.is_owner()
async def synccmd(ctx: commands.Context):
        bot.tree.copy_global_to(guild = ctx.guild)
        tmp = await bot.tree.sync(guild = ctx.guild)
        await ctx.send(f'Student debil przypomniał sobie {len(tmp)} komend!')

@bot.command(name = 'unsync')
@commands.is_owner()
async def unsynccmd(ctx: commands.Context):
        bot.tree.clear_commands(guild = ctx.guild)
        await bot.tree.sync(guild = ctx.guild)

@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extenstion):
        await bot.load_extension(f'cogs.{extenstion}')

@bot.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extenstion):
        await bot.unload_extension(f'cogs.{extenstion}')

@bot.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extenstion):
        await bot.unload_extension(f'cogs.{extenstion}')
        await bot.load_extension(f'cogs.{extenstion}')


@bot.event
async def on_guild_join(guild):
        '''
        When joining new guild bot will:
        1. Send welcome message
        2. Add administrator role with highest hierarchy
        3. Create a config channel for admins only 
        '''
        members = guild.members
        channels = guild.text_channels

        if channels == None:
                await guild.create_text_channel('ogólny')

        for i in channels:
                if (str(i.name).lower() == 'ogólny' or str(i.name).lower() == 'general'): 
                        await i.send('Student bot zatoczył się na Twój serwer!')
                        break
        
        overwrites = {}
        for i in guild.roles:
                overwrites[i] = d.PermissionOverwrite(read_messages = False)

        admin = await guild.create_role(name = 'Główny student debil', hoist = True, colour = d.Colour.gold())
        for i in members:
                if i.guild_permissions.administrator == True: await i.add_roles(admin)
        
        overwrites[admin] = d.PermissionOverwrite(read_messages = True)
        await guild.create_text_channel(name = 'ustawienia', overwrites = overwrites)

@bot.command(name = '')
@bot.listen('on_message')
async def background(ctx):
        cheers = ('jeb', 'pierdol', 'chuj')
        content = ctx.content.lower()
        channels = bot.get_all_channels()
        guild = bot.get_guild(ctx.guild.id)
        for i in cheers:
                if i in content:
                        await ctx.add_reaction('🍻')
        
@bot.command(name = 'clear')
async def clear_channel(ctx):
        if ctx.message.author.guild_permissions.administrator:
                await ctx.channel.purge()
        else:
                await ctx.channel.send('Niestety nie możesz siać masowej destrukcji :/')


async def POPIERDOLI_MNIE_ZARAZ():
        for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                        await bot.load_extension(f'cogs.{filename[:-3]}')


asyncio.run(POPIERDOLI_MNIE_ZARAZ())
bot.run(TOKEN)  
