import discord
from discord.ext import commands


from PyDictionary import PyDictionary


dictionary=PyDictionary()

#the greetings cog class
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the define function will define any word
    @commands.command()
    async def define(self, ctx, arg):
        """ - Gives the definition to any word"""
        obj = dictionary.meaning(arg)
        for key in obj:
            await ctx.send(key + ":")
            for definition in obj[key]:
                await ctx.send(definition)

def setup(client):
    client.add_cog(Info(client))