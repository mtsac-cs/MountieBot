import discord

from discord.ext import commands

#the greetings cog class
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the hello command. says hello back to the member by their name
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.send('Hello ' + member.name)

def setup(client):
    client.add_cog(Greetings(client))