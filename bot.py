import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger
import modules


class Bot:
    def __init__(self):
        self.__bot = commands.Bot(command_prefix='a*')
        self.__logger = logger.Logger('bot.py')

    def __load_modules(self):
        # Modules are hardcoded in modules.py, for now
        for module in modules.modules:
            self.__bot.load_extension(module)
            self.__logger.log_info(constants.MODULE_LOADED.format(module))

    def start_bot(self, token):
        self.__load_modules()
        self.__bot.run(token)

