"""Provide a template for making commands and a decorator to register them."""

from abc import abstractmethod, abstractclassmethod, ABCMeta

import argparse

from bot_help import HelpManager
from registrar import CommandRegistrar


def bot_command(cls):
    command = cls()

    if not issubclass(command.__class__, AbstractCommand):
        print(f'[ERROR] {command.__module__} is not a subclass of AbstractCommand and wont be loaded.')
        return

    command._parser = argparse.ArgumentParser(add_help=False)
    command._parser.add_argument(
        '-h', '--help',
        action='store_true',
        dest='help',
        default=False
    )
    command._parser.add_argument('args', nargs='*')

    old_exec = command.execute

    async def exec_hook(shards, client, msg):
        try:
            args, extra = command._parser.parse_known_args(msg.content.split()[1:])
            args = vars(args)
            if args['help']:
                await client.send_message(msg.channel, 'Help has been invoked')
                return
        except SystemExit as ex:
            await client.send_message(msg.channel, 'Something very very bad happened')
            return
    
        await old_exec(shards, client, msg)

    command.execute = exec_hook

    command_registrar = CommandRegistrar.instance()

    for alias in command.aliases:
        if alias.lower() not in command_registrar.command_table.keys():
            command_registrar.command_table[alias] = command
        else:
            print(f'Error: duplicate alias {alias.lower()} in {command.__module__}.py...')
            print(f'Duplicate is in {command_registrar.command_table[alias.lower()].__module__}')


class AbstractCommand(metaclass=ABCMeta):
    """Ensure all commands have a consistent interface"""

    @staticmethod
    @abstractclassmethod
    def execute(shards, shard, msg):
        """Executes this instances command"""
        raise NotImplementedError

    @property
    @abstractmethod
    def aliases(self):
        """The aliases that can be used to call this command"""
        raise NotImplementedError
