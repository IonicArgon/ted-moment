import datetime
import discord
from discord.ext import commands
from discord.ui import View, Button
from cogs.BaseCog import BaseCog

class GetCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.incident = None

    @commands.slash_command(name='get', description='Get an incident. Defaults to latest incident.')
    async def get(self, ctx: commands.Context, id: discord.Option(
        str,
        description='The ID of the incident.',
        required=False)) -> None:
        incident = None
        embed = self.base_embed.copy()
        embed.title += 'get incident'
        incident = None

        # if no ID, get latest incident
        if id is None:
            data = await self._get_log()
            if data is None or len(data) == 0:
                embed = self.base_embed.copy()
                embed.title += 'listing incidents'
                embed.description = 'Incident repository not initialized.'
                embed.color = discord.Color.red()
                await ctx.respond(embed=embed)
                return
            else:
                data.sort(key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
                id = data[0][3]
                incident = await self._get_incident(id)
        else:
            if len(id) != 6 or not id.isalnum():
                embed.description = 'Invalid ID.'
                embed.color = discord.Color.red()
                await ctx.respond(embed=embed)
                return
            
            incident = await self._get_incident(id)

        if incident is None:
            embed.description = 'No incident found with that ID.'
            embed.color = discord.Color.red()
        else:
            embed.add_field(name='Date', value=f'`{incident[0]}`', inline=True)
            embed.add_field(name='ID', value=f'`{incident[3]}`', inline=True)
            embed.add_field(name='Views', value=f'`{incident[4]}`', inline=True)
            embed.add_field(name='🤨 Count', value=f'`{incident[5]}`', inline=True)
            embed.add_field(name='🥵 Count', value=f'`{incident[6]}`', inline=True)
            embed.add_field(name=f'{incident[1]}', value=f'{incident[2]}', inline=False)

        # update views
        if incident is not None:
            incident[4] = str(int(incident[4]) + 1)
            await self._overwrite_row(id, incident)

        # add incident to class variable
        self.incident = incident

        # create voting buttons
        if incident is not None:
            view = View()
            bruh_button = Button(style=discord.ButtonStyle.gray, label='🤨', custom_id='bruh')
            rizz_button = Button(style=discord.ButtonStyle.gray, label='🥵', custom_id='rizz')
            bruh_button.callback = self._vote
            rizz_button.callback = self._vote
            view.add_item(bruh_button)
            view.add_item(rizz_button)

        if incident is not None:
            await ctx.respond(embed=embed, view=view)
        else:
            await ctx.respond(embed=embed)

    # callback for voting buttons
    async def _vote(self, interaction: discord.Interaction) -> None:
        # update votes
        if interaction.custom_id == 'bruh':
            self.incident[5] = str(int(self.incident[5]) + 1)
        elif interaction.custom_id == 'rizz':
            self.incident[6] = str(int(self.incident[6]) + 1)
        
        # update incident
        await self._overwrite_row(self.incident[3], self.incident)

        # send message
        await interaction.response.send_message('Vote counted.', ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GetCog(bot))