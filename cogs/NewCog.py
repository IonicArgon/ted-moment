import csv
import datetime
import logging
import secrets
import discord
from discord.ext import commands

class NewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.event_log = 'event_log.csv'

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('NewCog ready')

    @commands.slash_command(name='new', description='Create a new incident.')
    async def new(
        self, 
        ctx: commands.Context, 
        name: discord.Option(
            str,
            description='Name of the incident.',
            required=True),
        description: discord.Option(
            str,
            description='Description of the incident.',
            required=True),
        date: discord.Option(
            str,
            description='Date of the incident. Format: YYYY-MM-DD. Defaults to today.',
            required=False,
        default=None)):
        embed = discord.Embed(
            title='ted incident tracker | adding new incident',
            color=discord.Color.blue())
        embed.set_footer(
            text='Bot created by .extro',
            icon_url='https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024'
        )

        if date is None:
            date = datetime.date.today().strftime('%Y-%m-%d')
        else:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                embed.description = 'Invalid date format. Format: `YYYY-MM-DD`.'
                embed.color = discord.Color.red()
                await ctx.respond(embed=embed)
                return
            
        with open(self.event_log, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            event_id = ''.join(secrets.choice('0123456789ABCDEF') for i in range(6))
            writer.writerow([date, name, description, event_id])

        embed.description = f'New incident added: `{name}`.'
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(NewCog(bot))