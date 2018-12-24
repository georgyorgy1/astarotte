import os
import sys

import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger


class Owner:
    def __init__(self, bot):
        self.__bot = bot
        self.__logger = logger.Logger('owner.py')

    @commands.command()
    @commands.is_owner()
    async def restart(self, context):
        await context.send(constants.BOT_RESTART)
        self.__logger.log_info(constants.BOT_RESTART)
        os.execl(sys.executable, sys.executable, *sys.argv)
        await self.__bot.logout()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, context):
        await context.send(constants.BOT_SHUTDOWN)
        self.__logger.log_info(constants.BOT_SHUTDOWN)
        await self.__bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))

