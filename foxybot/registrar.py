

class CommandRegistrar():
    """A singleton to manage the command table and command execution"""

    _instance = None

    def __init__(self):
        self.command_table = {}

    @staticmethod
    def instance():
        """Get the singleton, create an instance if needed"""
        if not CommandRegistrar._instance:
            CommandRegistrar._instance = CommandRegistrar()
        return CommandRegistrar._instance

    @staticmethod
    async def execute_command(shards, shard, msg):
        instance = CommandRegistrar.instance()
        # !roll 100 -> 'roll'
        command = msg.content[1:].split()[0].lower()

        if command in instance.command_table.keys():
            await instance.command_table[command].execute(shards, shard, msg)


    @property
    def commands(self):
        return self.command_table

    @property
    def loaded_commands(self):
        return [command.name for command in set(self.command_table.values())]

    @property
    def loaded_aliases(self):
        return list(self.command_table.keys())
