import datetime
import secrets
import discord
import string
from discord.ext import commands
from cogs.BaseCog import BaseCog

class NewCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

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
            description='Date of the incident. Format: `YYYY-MM-DD`. Defaults to today.',
            required=False)) -> None:
        embed = self.base_embed.copy()
        embed.title += 'new'

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
            
        event_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(6))
        view_counter = 0
        bruh_counter = 0
        rizz_counter = 0
        await self._append_incident([date, name, description, event_id, view_counter, bruh_counter, rizz_counter])

        embed.description = f'New incident added.'
        embed.add_field(name='Name', value=f'`{name}`', inline=True)
        embed.add_field(name='Date', value=f'`{date}`', inline=True)
        embed.add_field(name='Event ID', value=f'`{event_id}`', inline=True)
        embed.add_field(name='Description', value=description, inline=False)
        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(NewCog(bot))