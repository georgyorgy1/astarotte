import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger


class Startup:
    def __init__(self, bot):
        self.__bot = bot
        self.__logger = logger.Logger('startup.py')

    async def on_ready(self):
        self.__logger.log_info('Astarotte has successfully logged in to Discord!')
        self.__logger.log_info(constants.SUCCESSFUL_LOGIN_USERNAME.format(self.__bot.user.name, self.__bot.user.discriminator))
        self.__logger.log_info(constants.SUCCESSFUL_LOGIN_USER_ID.format(str(self.__bot.user.id)))


def setup(bot):
    bot.add_cog(Startup(bot))

