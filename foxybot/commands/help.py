"""Command to retrieve help for other commands and topics"""

from discord import Embed

import utils

from command import AbstractCommand, bot_command
from registrar import CommandRegistrar
from bot_help import HelpManager
from config import conf

@bot_command
class Help(AbstractCommand):

    def __init__(self):
        self._aliases = ['help']

    async def execute(self, shards, client, msg):

        try:
            args, extra = self._parser.parse_known_args(msg.content.split()[1:])
        except SystemExit as ex:
            await client.send_message(msg.channel, 'Something very very bad happened')
            return

        args = vars(args)['args']
        name = args[0]
        num_args = len(args)
        lang = args[1] if num_args == 2 else 'en'

        command_table = CommandRegistrar.instance().commands
        
        if num_args not in (1, 2):
            usage = HelpManager.get_help(self._aliases[0])['usage']  \
                        .replace('{prefix}', conf['prefix'])
            await client.send_message(msg.channel, f"Usage: {usage}")
            return
            
        entry = HelpManager.get_help(name, lang=lang)

        if not entry:
            await client.message.send_message(msg.channel, "There is no help entry for that term.")
            return

        usage = entry['usage'].replace('{prefix}', conf['prefix'])
        description = entry['description']
        command = command_table[name]

        embed = Embed()
        embed.colour = 0x6699FF
        embed.title = f"**{name.capitalize()}**"
        embed.description = f"aliases: {', '.join(command.aliases)}"
        embed.set_thumbnail(url='https://i.imgur.com/MXkFjJj.png')
        embed.add_field(name=f"Usage:", value=usage, inline=False)
        embed.add_field(name="Description:", value=description, inline=False)
        embed.set_footer(text=f"Requested by {msg.author.name}#{msg.author.discriminator}",
                            icon_url=msg.author.avatar_url)

        await client.send_message(msg.channel, embed=embed)


    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
