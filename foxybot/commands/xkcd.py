"""Command to retrieve help for other commands and topics"""

import requests

from discord import Embed

from command import AbstractCommand, bot_command
from bot_help import HelpManager

@bot_command
class xkcd(AbstractCommand):
    _aliases = ['xkcd']

    async def execute(self, shards, client, msg):

        print("test?")

        # TODO: allow specifying a numbered comic or search term to retrieve
        url = requests.get('http://c.xkcd.com/random/comic/').url
        comic = requests.get(f'{url}/info.0.json').json()

        print(comic)

        embed = Embed()
        embed.colour = 0x6699FF
        embed.set_author(name=comic['title'], url=f"https://xkcd.com/{comic['num']}/")
        embed.set_image(url=comic['img'])
        embed.set_footer(text=comic['alt'])

        await client.send_message(msg.channel, embed=embed)



    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
