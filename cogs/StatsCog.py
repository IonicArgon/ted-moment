import datetime
import discord
from discord.ext import commands
from cogs.BaseCog import BaseCog

class StatsCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    @commands.slash_command(name='stats', description='Get global stats.')
    async def stats(self, ctx: commands.Context) -> None:
        data = await self._get_log()
        embed = self.base_embed.copy()
        embed.title += 'stats'

        # sort by date
        data = sorted(data, key=lambda x: x[0])

        # calculate days since last incident
        last_incident = datetime.datetime.strptime(data[-1][0], '%Y-%m-%d')
        today = datetime.datetime.today()
        days_since = (today - last_incident).days

        # calculate total incidents
        total_incidents = len(data)

        # calculate total views
        total_views = 0
        for incident in data:
            total_views += int(incident[4])

        # find most recent incident
        most_recent = data[-1][3]

        # find most viewed incident
        most_views = 0
        most_views_id = None
        for incident in data:
            if int(incident[4]) > most_views:
                most_views = int(incident[4])
                most_views_id = incident[3]

        # find most 🤨'd incident
        most_bruh = 0
        most_bruh_id = None
        for incident in data:
            if int(incident[5]) > most_bruh:
                most_bruh = int(incident[5])
                most_bruh_id = incident[3]

        # find most 🥵'd incident
        most_rizz = 0
        most_rizz_id = None
        for incident in data:
            if int(incident[6]) > most_rizz:
                most_rizz = int(incident[6])
                most_rizz_id = incident[3]

        # create embed
        embed.add_field(
            name='Total Incidents',
            value=f'`{total_incidents}`',
            inline=True
        )
        embed.add_field(
            name='Total Views',
            value=f'`{total_views}`',
            inline=True
        )
        embed.add_field(
            name='Days Since Last Incident',
            value=f'`{days_since}`',
            inline=True
        )

        bruh_incident = await self._get_incident(most_bruh_id)
        embed.add_field(
            name='Most 🤨\'d',
            value=f'`{bruh_incident[1]}` with `{most_bruh}` 🤨\'s',
            inline=True
        )

        rizz_incident = await self._get_incident(most_rizz_id)
        embed.add_field(
            name='Most 🥵\'d',
            value=f'`{rizz_incident[1]}` with `{most_rizz}` 🥵\'s',
            inline=True
        )

        views_incident = await self._get_incident(most_views_id)
        embed.add_field(
            name='Most Viewed',
            value=f'`{views_incident[1]}` with `{most_views}` views',
            inline=True
        )

        latest_incident = await self._get_incident(most_recent)
        embed.add_field(
            name=f'Latest Incident: {latest_incident[1]}',
            value=f'ID: `{latest_incident[3]}` \n Date: `{latest_incident[0]}` \n {latest_incident[2]}',
            inline=False
        )

        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(StatsCog(bot))