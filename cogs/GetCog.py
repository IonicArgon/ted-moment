import csv
import datetime
import logging
import discord
from discord.ext import commands

class GetCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.event_log = 'event_log.csv'
        self.base_embed = discord.Embed(
            title='ted incident tracker | ',
            color=discord.Color.blue())
        
        self.base_embed.set_footer(
            text='Bot created by .extro',
            icon_url='https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024'
        )

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('GetCog ready')

    @commands.slash_command(name='get', description='Get an incident by ID.')
    async def get(self, ctx: commands.Context, id: discord.Option(
        str,
        description='The ID of the incident.',
        required=True)):
        data = []
        embed = self.base_embed.copy()
        embed.title += 'get incident'

        # check if ID is right format, 6 length alphanumeric
        if len(id) != 6 or not id.isalnum():
            embed.description = 'Invalid ID.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return

        # check if event log exists and is not empty
        try:
            with open(self.event_log, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                if len(data) == 0:
                    embed.description = 'No incidents found.'
                    embed.color = discord.Color.red()
                    await ctx.respond(embed=embed)
                    return
        except FileNotFoundError:
            embed.description = 'No incidents found.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        
        # get incident by ID
        incident = None
        for row in data:
            if row[3] == id:
                incident = row
                break

        # create embed
        if incident is None:
            embed.description = 'No incident found with that ID.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        else:
            embed.add_field(name='Date', value=f'`{incident[0]}`', inline=True)
            embed.add_field(name='ID', value=f'`{incident[3]}`', inline=True)
            embed.add_field(name=f'{incident[1]}', value=f'{incident[2]}', inline=False)
            await ctx.respond(embed=embed)
            return
        
def setup(bot: commands.Bot):
    bot.add_cog(GetCog(bot))