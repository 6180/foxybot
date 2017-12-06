"""Just a test command"""

import utils
from command import AbstractCommand, bot_command
import discord

@bot_command
class Avatar(AbstractCommand):
    _aliases = ('avatar',)

    async def execute(self, shards, client, msg):

        try:
            args, extra = self._parser.parse_known_args(msg.content.split()[1:])
        except SystemExit:
            return

        args = vars(args)['args']

        if len(args) == 0:
            target = msg.author
        else:
            target = await utils.get_user(args[0], msg.channel.guild)

        if not target:
            await msg.channel.send("Unable to find user...")
            return

        await msg.channel.send(target)
        await msg.channel.send(target.avatar_url)

    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
