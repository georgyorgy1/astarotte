import json
import json.decoder
import math

import discord
import discord.ext.commands as commands
import discord.ext.commands.errors as errors

import lib.constants as constants
import lib.database as database


class CustomReaction(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._database = database.Database()

    def _is_integer(self, string):
        try:
            int(''.join(string))
            return True
        except ValueError:
            return False

    def _count_rows_as_pages(self, guild):
        statement =  "SELECT COUNT(*) FROM custom_commands WHERE guild = ?"
        result = self._database.execute_query(statement, (guild,))
        return int(math.ceil(float(list(result[0])[0] / 10)))

    def _create_embed(self, json_string):
        try:
            json_object = json.loads(''.join(json_string))
            embed = discord.Embed(color=json_object['color'])
            embed.set_image(url=str(json_object['image']))
            return embed
        except ValueError:
            return None
        except TypeError:
            return None
        return None

    # prevents the bot from throwing IndexError in the logs. Not a good solution but still a solution (a temporary one)
    def _is_result_empty(self, result):
        try:
            result_test = result[0]
            result_test = None # save ram
            return False
        except IndexError:
            return True

    def _reaction_id_exists(self, reaction_id, guild):
        statement = "SELECT * FROM custom_commands WHERE rowid = ? AND guild = ?"
        result = self._database.execute_query(statement, (reaction_id, guild))
        if self._is_result_empty(result):
            return False
        else:
            return True

    def _trigger_exists(self, reaction, guild):
        statement = "SELECT * FROM custom_commands WHERE command_name = ? AND guild = ?"
        result = self._database.execute_query(statement, (reaction, guild))
        if self._is_result_empty(result):
            return False
        else:
            return True

    def _get_requested_page(self, page):
        page_string = ''.join(page)
        if self._is_integer(page_string) == True:
            if int(page_string) <= 0:
                return ['0', '1']                
            else:
                return [str((int(page_string) - 1) * 10), page_string]
        else:
            return ['0', '1']

    def _get_custom_reaction(self, guild, trigger):
        statement = "SELECT response FROM custom_commands WHERE guild = ? AND command_name = ? ORDER BY RANDOM() LIMIT 1"
        result = self._database.execute_query(statement, (guild, trigger))
        if result != None and self._is_result_empty(result) == False:
            return result[0]
        else:
            return None

    @commands.command(aliases=['acr'])
    @commands.has_permissions(manage_guild=True)
    async def add_custom_reaction(self, context, trigger, *, reaction):
        if len(reaction) <= 120:
            statement = "INSERT INTO custom_commands VALUES (?, ?, ?)"
            success = self._database.execute_update(statement, (str(context.message.guild.id), trigger, str(reaction)))
            if success:
                await context.send(constants.ADD_CUSTOM_REACTION_SUCCESS.format(trigger, reaction))
            else:
                await context.send(constants.ADD_CUSTOM_REACTION_FAIL.format(trigger, reaction))
        else:
            await context.send('Too many characters. Limit is 120 characters (including spaces)')

    @commands.command(aliases=['lcr'])
    @commands.has_permissions(manage_guild=True)
    async def list_custom_reaction(self, context, *page):
        requested_page = self._get_requested_page(page) # 0: for SQL statement 1: the one the user entered
        statement = "SELECT rowid, command_name, response FROM custom_commands WHERE guild = ? LIMIT 10 OFFSET ?"
        guild = str(context.message.guild.id)
        results = self._database.execute_query(statement, (guild, requested_page[0]))
        total_pages = self._count_rows_as_pages(guild)
        if self._is_result_empty(results) == False:
            results_string = ''
            for result in results:
                results_string = results_string + constants.LIST_CUSTOM_REACTION_FORMAT.format(str(result[0]), str(result[1]), str(result[2]))
            pages_message_string = constants.LIST_CUSTOM_REACTION_PAGE_FORMAT.format(requested_page[1], str(total_pages))
            await context.send(results_string + '\n' + pages_message_string)
        else:
            await context.send('No custom reactions found')

    @commands.command(aliases=['dcr'])
    @commands.has_permissions(manage_guild=True)
    async def delete_custom_reaction(self, context, *reaction_id):
        reaction_id_string = ''.join(reaction_id)
        guild = str(context.message.guild.id)
        if self._is_integer(reaction_id_string):
            if self._reaction_id_exists(reaction_id_string, guild):
                statement = "DELETE FROM custom_commands WHERE rowid = ? AND guild = ?"
                success = self._database.execute_update(statement, (reaction_id_string, guild))
                if success:
                    await context.send(constants.DELETE_CUSTOM_REACTION_ID_SUCCESS.format(reaction_id_string))
                else:
                    await context.send(constants.DELETE_CUSTOM_REACTION_ID_FAIL.format(reaction_id_string))
            else:
                await context.send(constants.DELETE_CUSTOM_REACTION_INVALID_ID.format(reaction_id_string))
        else:
            await context.send(constants.DELETE_CUSTOM_REACTION_INVALID_INPUT.format(reaction_id_string))

    @commands.command(aliases=['pcr'])
    @commands.has_permissions(manage_guild=True)
    async def purge_custom_reactions(self, context, *, trigger):
        trigger_string = str(''.join(trigger))
        guild = str(context.message.guild.id)
        if self._trigger_exists(trigger_string, guild):
            statement = "DELETE FROM custom_commands WHERE command_name = ? AND guild = ?"
            success = self._database.execute_update(statement, (trigger_string, guild))
            if success:
                await context.send(constants.PURGE_CUSTOM_REACTIONS_SUCCESS.format(trigger_string))
            else:
                await context.send(constants.PURGE_CUSTOM_REACTIONS_FAIL.format(trigger_string))
        else:
            await context.send(constants.PURGE_CUSTOM_REACTIONS_INVALID_TRIGGER.format(trigger_string))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            custom_reaction = self._get_custom_reaction(str(message.guild.id), str(message.content))
            if custom_reaction != None:
                embed = self._create_embed(custom_reaction)
                if embed != None:
                    await message.channel.send("", embed=embed)
                else: 
                    await message.channel.send(''.join(custom_reaction))


def setup(bot):
    bot.add_cog(CustomReaction(bot))

