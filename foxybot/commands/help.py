"""Command to retrieve help for other commands and topics"""


from command import AbstractCommand, bot_command
from bot_help import HelpManager

@bot_command
class Help(AbstractCommand):
    _aliases = ('help', 'h')

    async def execute(self, shards, client, msg):

        try:
            args, extra = self._parser.parse_known_args(msg.content.split()[1:])
        except SystemExit as ex:
            await client.send_message(msg.channel, 'Something very very bad happened')
            return
 
        # await client.send_message(msg.channel, (args, extra))
        await client.send_message(msg.channel, "Hello, World!")


    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
