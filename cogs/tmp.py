from discord.ext import commands
import discord as d

import asyncio

class Temporary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.time = 5

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def tmp(self, ctx: commands.Context, time = 5):
        '''
        Tworzy kanał tmp, student debil ma pamięć trwającą domyślnie 5 minut
        '''
        try: time = int(time) if int(time) <= 30 else 5
        except: time = 5
        self.time = time

        guild = self.bot.get_guild(ctx.guild.id)
        channels = self.bot.get_all_channels()
        
        chan_names = (str(x.name).lower() for x in channels)
        if 'tmp' not in chan_names:
                await guild.create_text_channel('tmp')
        

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if str(ctx.channel.name) == 'tmp': await cooldown(ctx, self.time)

    @commands.command(name ='czas_tmp')
    @commands.has_permissions(manage_channels = True)
    async def change_cooldown(self, ctx, time):
        '''
        Pozwala zmienić cooldown kanału tmp
        '''
        try: 
            self.time = int(time) if int(time) <= 30 else self.time
        except ValueError: ctx.send("Studencie debilu, czas musi być liczbą!")

async def cooldown(ctx, time):
    await asyncio.sleep(time*60)
    try:
        await ctx.delete()
    except LookupError:
        print("Internal Lookup Error: msg no longer exists")


async def setup(bot):
    await bot.add_cog(Temporary(bot))




            
