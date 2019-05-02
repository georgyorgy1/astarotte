import discord.ext.commands as commands

import lib.constants as constants
import lib.logger as logger


class Startup(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._logger = logger.Logger('startup.py')
    
    @commands.Cog.listener()
    async def on_ready(self):
        self._logger.log_info('Astarotte has successfully logged in to Discord!')
        self._logger.log_info(constants.SUCCESSFUL_LOGIN_USERNAME.format(self._bot.user.name, self._bot.user.discriminator))
        self._logger.log_info(constants.SUCCESSFUL_LOGIN_USER_ID.format(str(self._bot.user.id)))


def setup(bot):
    bot.add_cog(Startup(bot))

