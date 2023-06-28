import discord
from discord.ext import commands

class HelpCog(commands.Cog, name='Help'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.all_commands = {
            'help': {'value': 'List all commands.'},
            'new': {
                'value': 'Create a new incident.', 
                'options': [
                    'name', 'required', 'Name of the incident.',
                    'description', 'required', 'Description of the incident.',
                    'date', 'optional', 'Date of the incident. Format: `YYYY-MM-DD`. Defaults to today.',
                ]},
            'list': {'value': 'List all incidents.'},
            'last': {'value': 'Get the last incident.'},
            'days': {'value': 'Display the number of days since the last incident.'},
            'get': {
                'value': 'Get an incident by ID.',
                'options': ['id', 'required', 'ID of the incident.']
                },
        }

    async def _default_help(self, embed):
        value_ = ''
        for command in self.all_commands:
            value_ += f'- {command}\n'

        embed.add_field(
            name='General Commands',
            value=value_,
            inline=False)
        
    async def _help(self, embed, command):
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
        required=False)):
        embed = discord.Embed(
            title='ted incident tracker | help',
            color=discord.Color.blue())
        
        embed.set_footer(
            text='Bot created by .extro',
            icon_url='https://cdn.discordapp.com/avatars/244948020569964545/553692a2ef6f042857754748630170f5?size=1024'
        )

        if command is None:
            embed.description = 'List of commands for the `ted incident tracker` bot.'
            await self._default_help(embed)
        else:
            if command not in self.all_commands:
                embed.description = f'Command `{command}` not found.'
                embed.color = discord.Color.red()
                await ctx.respond(embed=embed)
                return
            
            embed.title = f'ted incident tracker | help {command}'
            await self._help(embed, command)

        await ctx.respond(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))