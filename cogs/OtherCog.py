import csv
import datetime
import logging
import discord
from discord.ext import commands

class OtherCogs(commands.Cog):
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
        logging.info('OtherCogs ready')

    @commands.slash_command(name='last', description='Get the last incident.')
    async def last(self, ctx: commands.Context):
        data = []

        # check if event log exists and is not empty
        try:
            with open(self.event_log, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                if len(data) == 0:
                    embed = self.base_embed.copy()
                    embed.title += 'last incident'
                    embed.description = 'No incidents found.'
                    embed.color = discord.Color.red()
                    await ctx.respond(embed=embed)
                    return
        except FileNotFoundError:
            embed = self.base_embed.copy()
            embed.title += 'last incident'
            embed.description = 'No incidents found.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        
        # sort by date from newest to oldest
        data.sort(key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)

        # get last incident
        last_incident = data[0]

        # create embed
        embed = self.base_embed.copy()
        embed.title += 'last incident'
        embed.add_field(name='Date', value=f'`{last_incident[0]}`', inline=True)
        embed.add_field(name='ID', value=f'`{last_incident[3]}`', inline=True)
        embed.add_field(name=f'{last_incident[1]}', value=f'{last_incident[2]}', inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command(name='days', description='Display the days since the last incident.')
    async def days(self, ctx: commands.Context):
        data = []

        # check if event log exists and is not empty
        try:
            with open(self.event_log, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                if len(data) == 0:
                    embed = self.base_embed.copy()
                    embed.title += 'days since last incident'
                    embed.description = 'No incidents found.'
                    embed.color = discord.Color.red()
                    await ctx.respond(embed=embed)
                    return
        except FileNotFoundError:
            embed = self.base_embed.copy()
            embed.title += 'days since last incident'
            embed.description = 'No incidents found.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        
        # sort by date from newest to oldest
        data.sort(key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)

        # get last incident
        last_incident = data[0]

        # get days since last incident
        today = datetime.datetime.today()
        last_incident_date = datetime.datetime.strptime(last_incident[0], '%Y-%m-%d')
        days_since_last_incident = (today - last_incident_date).days

        # create embed
        embed = self.base_embed.copy()
        embed.title += 'days since last incident'
        embed.description = f'It has been `{days_since_last_incident}` days since the last incident.'

        await ctx.respond(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(OtherCogs(bot))