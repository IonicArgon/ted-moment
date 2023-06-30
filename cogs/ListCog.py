import discord
import datetime
from discord.ext import commands
from discord.ext.pages import Page, Paginator, PaginatorButton
from cogs.BaseCog import BaseCog

class ListCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.slash_command(name='list', description='List all incidents.')
    async def list(self, ctx: commands.Context):
        data = await self._get_log()
        pages = []

        if data is None or len(data) == 0:
            embed = self.base_embed.copy()
            embed.title += 'listing incidents'
            embed.description = 'Incident repository not initialized.'
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        
        # sort by date from newest to oldest
        data.sort(key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)

        # create pages of 5 incidents each
        for i in range(0, len(data), 5):
            embed = self.base_embed.copy()
            embed.title += 'listing incidents'
            for row in data[i:i+5]:
                embed.add_field(
                    name=f'{row[0]} | {row[1]}',
                    value=f'`ID:` {row[3]}\n{row[2]}',
                    inline=False
                )
            pages.append(Page(embeds=[embed]))

        paginator = Paginator(pages)

        # add buttons to paginator
        paginator.add_button(PaginatorButton('prev', label='◀️', style=discord.ButtonStyle.blurple))
        paginator.add_button(PaginatorButton('page_indicator', style=discord.ButtonStyle.gray, disabled=True))
        paginator.add_button(PaginatorButton('next', label='▶️', style=discord.ButtonStyle.blurple))

        paginator.remove_button('first')
        paginator.remove_button('last')

        await paginator.respond(ctx.interaction)

def setup(bot: commands.Bot):
    bot.add_cog(ListCog(bot))
