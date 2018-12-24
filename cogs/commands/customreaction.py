import json
import json.decoder
import sqlite3

import discord
import discord.ext.commands as commands

import lib.database as database
import lib.logger as logger 


class CustomReaction:
    def __init__(self, bot):
        self.__bot = bot
        self.__database = database.Database()
        self.__logger = logger.Logger('customreaction.py')

    def __create_embed(self, json_string):
        try:
            json_object = json.loads(json_string)
            embed = discord.Embed(color=json_object['color'])
            embed.set_image(url=str(json_object['image']))
            return embed
        except ValueError:
            return None
        return None

    def __get_custom_reaction(self, guild, trigger):
        statement = '''SELECT response FROM custom_commands WHERE guild = ? AND command_name = ? ORDER BY RANDOM() LIMIT 1'''
        result = self.__database.retrieve_single_result(statement, (guild, trigger))
        if result != None:
            return result[0]
        else:
            return None

    async def on_message(self, message):
        if message.author.bot == False:
            custom_reaction = self.__get_custom_reaction(str(message.guild.id), str(message.content))
            if custom_reaction != None:
                embed = self.__create_embed(custom_reaction)
                if embed != None:
                    await message.channel.send("", embed=embed)
                else: 
                    await message.channel.send(custom_reaction)


def setup(bot):
    bot.add_cog(CustomReaction(bot))

