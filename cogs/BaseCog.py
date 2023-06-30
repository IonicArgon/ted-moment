import csv
import logging
import discord
import typing
from discord.ext import commands

class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
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
    async def on_ready(self) -> None:
        logging.info(f'{self.__class__.__name__} ready')

    async def _get_log(self) -> typing.Optional[list]:
        data = None
        try:
            with open(self.event_log, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)

                if len(data) == 0:
                    data = []
        except FileNotFoundError:
            pass

        return data
    
    async def _get_incident(self, id: str) -> typing.Optional[list]:
        data = await self._get_log()
        incident = None

        if data is not None:
            for row in data:
                if row[3] == id:
                    incident = row
                    break

        return incident
    
    # append incident to log
    async def _append_incident(self, incident: list) -> None:
        with open(self.event_log, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(incident)

    # overwrite log with new data
    async def _overwrite_log(self, data: list) -> None:
        with open(self.event_log, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    # overwrite one row in log by ID
    async def _overwrite_row(self, id: str, row: list) -> None:
        data = await self._get_log()

        if data is not None:
            for i in range(len(data)):
                if data[i][3] == id:
                    data[i] = row
                    break

        await self._overwrite_log(data)

    
def setup(bot: commands.Bot) -> None:
    bot.add_cog(BaseCog(bot))