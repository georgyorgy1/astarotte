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
        try:
            connection = self.__database.create_connection()
            cursor = connection.cursor()
            statement = '''SELECT response FROM custom_commands WHERE guild = ? AND command_name = ? ORDER BY RANDOM() LIMIT 1'''

            cursor.execute(statement, (guild, trigger))
            text_reaction = cursor.fetchone()

            if text_reaction != None:
                return text_reaction[0]
            else:
                return None
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
        finally:
            self.__database.close_connection(connection)
        return None

    async def on_message(self, message):
        if message.author.bot == False:
            reaction = self.__get_custom_reaction(str(message.guild.id), str(message.content)) # if message.author.bot == False else return
            if reaction != None:
                embed = self.__create_embed(reaction) # if reaction != None else return
                if embed != None:
                    await message.channel.send("", embed=embed) # if embed != None else await message.channel.send(reaction)
                else:
                    await message.channel.send(reaction)


def setup(bot):
    bot.add_cog(CustomReaction(bot))

