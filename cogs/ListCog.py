import csv
import datetime
import logging
import discord
from discord.ext import commands
from discord.ext.pages import Page, Paginator, PaginatorButton

class ListCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.event_log = 'event_log.csv'
        self.base_embed = discord.Embed(
            title='ted incident tracker | listing incidents',
            color=discord.Color.blue())
        
        self.base_embed.set_footer(
            text='Bot created by .extro',
            icon_url='https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024'
        )

        self.base_paginator_buttons = [
            PaginatorButton('prev', label='◀️', style=discord.ButtonStyle.blurple),
            PaginatorButton('page_indicator', style=discord.ButtonStyle.gray, disabled=True),
            PaginatorButton('next', label='▶️', style=discord.ButtonStyle.blurple)
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('ListCog ready')

    @commands.slash_command(name='list', description='List all incidents.')
    async def list(self, ctx: commands.Context):
        data = []
        pages = []

        # check if event log exists and is not empty
        try:
            with open(self.event_log, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                if len(data) == 0:
                    embed = self.base_embed.copy()
                    embed.description = 'No incidents found.'
                    embed.color = discord.Color.red()
                    await ctx.respond(embed=embed)
                    return
        except FileNotFoundError:
            embed = self.base_embed.copy()
            embed.description = 'No incidents found.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        
        # sort by date from newest to oldest
        data.sort(key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)

        # create pages of 5 incidents each
        for i in range(0, len(data), 5):
            embed = self.base_embed.copy()
            for row in data[i:i+5]:
                embed.add_field(
                    name=f'{row[0]} | {row[1]}',
                    value=f'`ID:` {row[3]}\n{row[2]}',
                    inline=False)
            pages.append(Page(embeds=[embed]))

        paginator = Paginator(pages)

        # add buttons to paginator
        for button in self.base_paginator_buttons:
            paginator.add_button(button)

        paginator.remove_button('first')
        paginator.remove_button('last')

        await paginator.respond(ctx.interaction)

def setup(bot: commands.Bot):
    bot.add_cog(ListCog(bot))