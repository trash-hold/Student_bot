from discord.ext import commands
from discord import app_commands

import discord as d

import asyncio

def permit_check(interaction: d.Interaction) -> bool:
    return interaction.permissions.manage_channels

class Temporary(commands.GroupCog, name = 'tmp'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.time = 5
        self.tmp = None

    @commands.hybrid_command(name = 'dodaj')
    @app_commands.describe(time = 'czas w min')
    @app_commands.check(permit_check)
    async def create(self, interaction: d.Interaction, time: int = 5) -> None:
        '''
        Tworzy kanał tmp, student debil ma pamięć trwającą domyślnie 5 minut
        '''
        try: time = int(time) if int(time) <= 30 else 5
        except: time = 5
        self.time = time

        guild = interaction.guild
        channels = self.bot.get_all_channels()

        for x in channels:
            if str(x.name).lower() == 'tmp':
                print('Found tmp') 
                await interaction.response.send_message(content = 'Kanał tmp został przejęty przez bota!', ephemeral=True)
                self.tmp = x
                await self.tmp.send(content='To tutaj tracę wspomnienia...')
                break
        
        if self.tmp is None:
            print('Tworzę kanał')
            self.tmp = await guild.create_text_channel('tmp')
            await interaction.response.send_message(content = 'Kanał tmp utworzony!', ephemeral = True)
        

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context) -> None:
        if ctx.channel == self.tmp: await cooldown(ctx, self.time)

    @app_commands.command(name ='timer')
    @app_commands.describe(time = 'czas w min')
    @app_commands.check(permit_check)
    async def change_cooldown(self, interaction: d.Interaction, time: int) -> None:
        '''Pozwala zmienić okres czyszczenia wiadomości (w minutach)'''
        try: 
            self.time = int(time) if int(time) <= 30 else self.time
            await interaction.response.send_message(f'Student debil ma teraz pamięć o długości {str(self.time)} minut!', ephemeral = True)

        except ValueError: await interaction.response.send_message("Studencie debilu, czas musi być liczbą całkowitą!", ephemeral = True)

    
    @app_commands.command(name = 'usuń')
    @app_commands.check(permit_check)
    async def delete_tmp(self, interaction: d.Interaction) -> None:
        '''Usuwa kanał tmp'''
        if self.tmp is not None:
            try: 
                await self.tmp.delete()
                await interaction.response.send_message(content = 'Kanał tmp został usunięty', ephemeral = True )
            except: await interaction.response.send_message(content = 'Coś kombinowałeś przy kanale prawda?', ephemeral = True )
        else: await interaction.response.send_message(content = 'Kanał tmp nie został jeszcze utworzony ;/', ephemeral = True)


async def cooldown(ctx: commands.Context, time: int) -> None:
    '''Delays message delation by given time'''
    await asyncio.sleep(time*60)
    try:
        await ctx.delete()
    except LookupError:
        print("Internal Lookup Error: msg no longer exists")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Temporary(bot))




            
