import discord.ext.commands as commands

import lib.constants as constants


class Fun(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    def _reverse(self, string):
        return string[::-1]

    def _get_api_latency(self):
        latency = int(self._bot.latency * 1000)
        return str(latency)

    @commands.command()
    async def ping(self, context):
        # Latency is in ms (seconds * 1000)
        await context.send(constants.BOT_LATENCY.format(self._get_api_latency()))

    @commands.command()
    async def palindrome(self, context, word):
        await context.send(constants.WORD_IS_PALINDROME.format(word) if word == self._reverse(word) else constants.WORD_IS_NOT_PALINDROME.format(word))


def setup(bot):
    bot.add_cog(Fun(bot))

