import json
import json.decoder
import os
import sys
import time

import discord.ext.commands as commands
import psutil

import lib.constants as constants
import lib.jsonfile as jsonfile


class Info:
    def __init__(self, bot):
        self.__bot = bot
        self.__start_time = time.time()

    def __get_bot_uptime(self):
        raw_seconds = int(time.time() - self.__start_time)
        raw_minutes = int(raw_seconds / 60)        
        raw_hours = int(raw_seconds / 3600)
        seconds = int(raw_seconds % 60) if raw_seconds >= 60 and raw_minutes >= 1 else raw_seconds
        minutes = int(raw_minutes % 60) if raw_minutes >= 60 and raw_hours >= 1 else raw_minutes
        hours = int(raw_hours % 24) if raw_hours >= 24 else raw_hours
        days = int(raw_seconds / 86400)
        return constants.BOT_UPTIME.format(str(days), str(hours), str(minutes), str(seconds))

    def __get_memory_usage(self):
        return str(int((psutil.Process(os.getpid()).memory_info().rss / 1048576))) # 1 MB = 1048576 Bytes

    def __get_python_version(self):
        return str(sys.version).replace('\n', '')

    def __get_bot_json_info(self, key):
        json_file = jsonfile.JSONFile('info.json')
        bot_info = json_file.get_json_file()
        return bot_info[key]
        
    @commands.command()
    async def stats(self, context):
        bot_name = self.__get_bot_json_info('bot_name')
        build = self.__get_bot_json_info('build')
        python_version = self.__get_python_version()
        memory_usage = self.__get_memory_usage()
        author = self.__get_bot_json_info('author')
        uptime = self.__get_bot_uptime()
        await context.send(constants.BOT_STATS.format(bot_name, build, python_version, memory_usage, author, uptime))


def setup(bot):
    bot.add_cog(Info(bot))

