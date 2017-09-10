"""Provide a template for making commands and a decorator to register them."""

from abc import abstractmethod, abstractclassmethod, ABCMeta
from enum import Enum

from registrar import CommandRegistrar

def bot_command(cls):
    command = cls()

    if not issubclass(command.__class__, AbstractCommand):
        print(f'[ERROR] {command.__module__} is not a subclass of AbstractCommand and wont be loaded.')
        return

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
