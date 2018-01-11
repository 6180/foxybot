"""Provide a class to load and parse the help file and 
Provide a simple interface for retrieving help entries"""

import json
import os

from config import conf
import utils
from discord.embeds import Embed
from registrar import CommandRegistrar


class HelpManager(object):
    _help_dict = {}
    _last_modified = 0

    @staticmethod
    def get_help(key, lang='en'):
        """ Retrieve a given commands help text with given language.
        :param lang: ISO 639-1 language code specifying language to try to retrieve
        :param key: name of the command
        :return: description in `lang` for `key`
        """

        if os.path.getmtime('help.json') > HelpManager._last_modified:
            HelpManager.load_help()

        lang = lang.lower()
        key = key.lower()

        if lang not in HelpManager._help_dict:
            print(f"[ERROR] tried to access `_help_dict[{lang}]`")
            lang = 'en'


        if key not in HelpManager._help_dict[lang]:
            print(f"[ERROR] tried to access `_help_dict[{lang}][{key}]`")
            return None

        return HelpManager._help_dict[lang][key]

    @staticmethod
    def load_help():
        try:
            with open('help.json', 'r', encoding='utf-8') as infile:
                HelpManager._help_dict = json.load(infile)
                HelpManager._last_modified = os.path.getmtime('help.json')
        except OSError as ex:
            print("[ERROR] Cannot find `help.json`")
            print(ex)

    @staticmethod
    async def get_help_embed(command, msg_content, author):
        raw_args = await utils.get_args(command, msg_content)
        args = raw_args['args']
        num_args = len(args)

        embed = Embed()
        embed.colour = author.colour

        if num_args not in (1, 2) and not raw_args['help']:
            usage = HelpManager.get_help(command._aliases[0])['usage'].replace('{prefix}', conf['prefix'])
            embed.add_field(name="Usage:", value=usage, inline=False)
            return embed
        elif raw_args['help']:
            name = msg_content.split()[0][1:]
            lang = 'en'
        else:
            name = args[0]
            lang = args[1] if num_args == 2 else 'en'

        entry = HelpManager.get_help(name, lang=lang)

        if not entry:
            if name in CommandRegistrar.instance().command_table.keys():
                embed.title = f":octagonal_sign: There is no '{lang}' translation for '{name}'. :octagonal_sign:"
            else:
                embed.title = ":octagonal_sign: That doesnt seem to be a valid command. :octagonal_sign:"
                print("Cunt...")

            return embed

        usage = entry['usage'].replace('{prefix}', conf['prefix'])
        description = entry['description']
        command_table = CommandRegistrar.instance().commands
        command = command_table[name]

        embed.title = f"**{name}**"
        embed.description = f"aliases: {', '.join(command.aliases)}"
        embed.set_thumbnail(url='https://i.imgur.com/MXkFjJj.png')
        embed.add_field(name="Usage:", value=usage, inline=False)
        embed.add_field(name="Description:", value=description, inline=False)
        embed.set_thumbnail(url='https://i.imgur.com/MXkFjJj.png')
        embed.set_footer(text=f"Requested by {author.name}#{author.discriminator}",
                         icon_url=author.avatar_url)
        return embed
