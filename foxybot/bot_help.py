"""Provide a class to load and parse the help file and 
Provide a simple interface for retrieving help entries"""

import json
import os


class HelpManager(object):
    _help_dict = {}
    _last_modified = 0

    @staticmethod
    def get_help(lang, key):
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

        print(HelpManager._help_dict)
