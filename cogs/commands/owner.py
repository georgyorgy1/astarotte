import os
import sys

import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger


class Owner(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._logger = logger.Logger('owner.py')

    @commands.command()
    @commands.is_owner()
    async def restart(self, context):
        await context.send(constants.BOT_RESTART)
        self._logger.log_info(constants.BOT_RESTART)
        os.execl(sys.executable, sys.executable, *sys.argv)
        await self._bot.logout()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, context):
        await context.send(constants.BOT_SHUTDOWN)
        self._logger.log_info(constants.BOT_SHUTDOWN)
        await self._bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))

