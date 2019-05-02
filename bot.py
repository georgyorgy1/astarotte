import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger
import modules


class Bot:
    def __init__(self):
        self._bot = commands.Bot(command_prefix='a*')
        self._logger = logger.Logger('bot.py')

    def _load_modules(self):
        # Modules are hardcoded in modules.py, for now
        for module in modules.modules:
            self._bot.load_extension(module)
            self._logger.log_info(constants.MODULE_LOADED.format(module))

    def start_bot(self, token):
        self._load_modules()
        self._bot.run(token)

