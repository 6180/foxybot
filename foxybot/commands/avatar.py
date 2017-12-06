"""Just a test command"""

import utils
from command import AbstractCommand, bot_command
from discord import embeds

@bot_command
class Avatar(AbstractCommand):
    _aliases = ('avatar',)

    async def execute(self, shards, client, msg):

        args = await utils.get_args(self, msg)

        if len(args) == 0:
            target = msg.author
        else:
            target = await utils.get_user(args[0], msg.channel.guild)

        if not target:
            await msg.channel.send("Unable to find user...")
            return

        embed = embeds.Embed()
        embed.colour = target.colour
        embed.set_author(name=f"{target.display_name}'s avatar", url=target.avatar_url)
        embed.set_image(url=target.avatar_url)
        embed.set_footer(text=f"Requested by {msg.author.display_name}#{msg.author.discriminator}",
                         icon_url=msg.author.avatar_url)

        await msg.channel.send(embed=embed)

    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
