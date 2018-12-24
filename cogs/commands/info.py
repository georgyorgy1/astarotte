import json
import json.decoder
import os
import sys
import time

import discord.ext.commands as commands
import psutil

import lib.constants as constants
import lib.jsonfile as jsonfile
import lib.logger as logger


class Info:
    def __init__(self, bot):
        self.__bot = bot
        self.__start_time = time.time()
        self.__logger = logger.Logger('info.py')
        self.__json_file = jsonfile.JSONFile('info.json')
        self.__bot_info = self.__json_file.get_json_file()

    def __get_bot_uptime(self):
        seconds = int(time.time() - self.__start_time)
        minutes = int(seconds / 60)        
        hours = int(seconds / 3600)
        days = int(seconds / 86400)

        if seconds >= 60 and minutes >= 1:
            seconds = int(seconds % 60)
        if minutes >= 60 and hours >= 1:
            minutes = int(minutes % 60) 
        if hours >= 24:
            hours = int(hours % 24)

        return constants.BOT_UPTIME.format(str(days), str(hours), str(minutes), str(seconds))

    @commands.command(name='stats')
    async def get_bot_dev_stats(self, context):
        # the necessary info
        bot_name = self.__bot_info['bot_name']
        build = self.__bot_info['build']
        python_version = str(sys.version).replace('\n', '')
        memory_usage = str(int((psutil.Process(os.getpid()).memory_info().rss / 1048576)))
        author = self.__bot_info['author']
        uptime = self.__get_bot_uptime()

        await context.send(constants.BOT_STATS.format(bot_name, build, python_version, memory_usage, author, uptime))


def setup(bot):
    bot.add_cog(Info(bot))

