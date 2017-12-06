"""Command to retrieve random xkcd comic"""

import requests

from discord import Embed

from command import AbstractCommand, bot_command

@bot_command
class Xkcd(AbstractCommand):
    _aliases = ['xkcd']

    async def execute(self, shards, client, msg):
        # TODO: allow specifying a numbered comic or search term to retrieve
        url = requests.get('http://c.xkcd.com/random/comic/').url
        comic = requests.get(f'{url}/info.0.json').json()

        embed = Embed()
        embed.colour = 0x6699FF
        embed.set_author(name=comic['title'], url=f"https://xkcd.com/{comic['num']}/")
        embed.set_image(url=comic['img'])
        embed.set_footer(text=comic['alt'])

        await msg.channel.send(embed=embed)

    @property
    def aliases(self):
        return self._aliases
