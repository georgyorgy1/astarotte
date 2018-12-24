import discord.ext.commands as commands

import lib.constants as constants


class Fun:
    def __init__(self, bot):
        self.__bot = bot

    def __reverse(self, string):
        return string[::-1]

    @commands.command()
    async def ping(self, context):
        # Latency is in ms (seconds * 1000)
        await context.send(constants.BOT_LATENCY.format(str(int(self.__bot.latency * 1000))))

    @commands.command()
    async def palindrome(self, context, word):
        await context.send(constants.WORD_IS_PALINDROME.format(word) if word == self.__reverse(word) else constants.WORD_IS_NOT_PALINDROME.format(word))

def setup(bot):
    bot.add_cog(Fun(bot))

