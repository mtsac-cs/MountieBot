import discord

from discord.ext import commands
from discord.utils import get

client = discord.Client()

#the roles cog class
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the define function will define any word
    @commands.command()
    async def iam(self, ctx, arg = ''):
        """ - Set Role of user(Test)"""

        member = ctx.message.author
        arg = arg.upper()

        if arg == '':
            await ctx.send("No Role Specified")

        else: 
            if arg == 'TEST':
                role = get(member.guild.roles, name = arg)
                await member.add_roles(role, reason='Bot Call')

def setup(client):
    client.add_cog(Roles(client))