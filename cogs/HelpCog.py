import discord
from discord.ext import commands
from cogs.BaseCog import BaseCog

class HelpCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.all_commands = {
            'help': {
                'value': 'List all commands.',
                'options': [
                    'command', 'optional', 'The command to get help for.',
                    ]
                },
            'new': {
                'value': 'Create a new incident.', 
                'options': [
                    'name', 'required', 'Name of the incident.',
                    'description', 'required', 'Description of the incident.',
                    'date', 'optional', 'Date of the incident. Format: `YYYY-MM-DD`. Defaults to today.',
                ]},
            'list': {'value': 'List all incidents.'},
            'stats': {'value': 'Gets global stats.'},
            'get': {
                'value': 'Get an incident by ID.',
                'options': ['id', 'optional', 'ID of the incident. Format: `XXXXXX` alphanumeric. Defaults to the last incident.']
                },
        }

    async def _default_help(self, embed) -> None:
        embed.description = 'List of commands for the `ted incident tracker` bot.'

        value_ = ''
        for command in self.all_commands:
            value_ += f'- {command}\n'

        embed.add_field(
            name='General Commands',
            value=value_,
            inline=False)
        
    async def _help(self, embed, command) -> None:
        embed.title += f' {command}'
        embed.description = self.all_commands[command]['value']
        
        if 'options' in self.all_commands[command]:
            value_ = ''
            for i in range(0, len(self.all_commands[command]['options']), 3):
                value_ += f'`{self.all_commands[command]["options"][i]}` - *{self.all_commands[command]["options"][i+1]}*, {self.all_commands[command]["options"][i+2]}\n'
            embed.add_field(
                name='Options',
                value=value_,
                inline=False)
    
    @commands.slash_command(name='help', description='List all commands.')
    async def help(self, ctx: commands.Context, command: discord.Option(
        str, 
        description='The command to get help for.',
        required=False)) -> None:
        embed = self.base_embed.copy()
        embed.title += ' help'

        if command is None:
            await self._default_help(embed)
        else:
            if command not in self.all_commands:
                embed.description = f'Command `{command}` not found.'
                embed.color = discord.Color.red()
            else:
                await self._help(embed, command)

        await ctx.respond(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelpCog(bot))