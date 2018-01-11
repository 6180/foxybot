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
        embed = await HelpManager.get_help_embed(self, msg.content, msg.author)
        await msg.channel.send(embed=embed)

    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
