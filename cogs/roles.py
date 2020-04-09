import discord

from discord.ext import commands
from discord.utils import get


import os
import sys

import pymysql.cursors
import json


client = discord.Client()

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import config

defaultSelfRole = "TEST"

#function to update self assignable roles in remote mysql database
def updateSelfRoles():
	if config.sqlConnected:
		try:
			connection = pymysql.connect(host=config.server_info["ip"],
										user=config.server_info["database"]["user"],
										password=config.server_info["database"]["password"],
										db=config.server_info["database"]["name"],
										charset='utf8mb4',
										cursorclass=pymysql.cursors.DictCursor
			)
			try:
				with connection.cursor() as cursor:
					#getting the self assignable roles dictionary as a string
					s_roles = json.dumps(config.self_assignable_roles, separators=(',', ':'))
					#updating the database
					sql = "UPDATE `selfroles` SET `rolenames` = %s LIMIT 1;"
					cursor.execute(sql, (s_roles))
			finally:
				connection.commit()
				connection.close()
		except:
			print("Failed to update database.")



#the roles cog class
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the define function will define any word
    @commands.command()
    async def iam(self, ctx, arg = ''):
        """ - Gives self assignable role"""

        member = ctx.message.author

        if not str(ctx.guild.id) in config.self_assignable_roles:
            config.self_assignable_roles[str(ctx.guild.id)] = [defaultSelfRole]

        if arg == '':
            await ctx.send("No Role Specified")

        else: 
            if arg in config.self_assignable_roles[str(ctx.guild.id)]:
                rolefound = False
                for grole in member.guild.roles:
                    if grole.name == arg:
                        rolefound = True
                        role = get(member.guild.roles, name = arg)
                        await member.add_roles(role, reason='Bot Call')
                        await ctx.send("Role set.")
                if not rolefound:
                    await ctx.send(arg + " is not a role")
            else:
                await ctx.send(arg + " is not a self assignable role")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def selfrole(self, ctx, arg=''):
        """" - Add a self assignable role (admin)"""
        if not str(ctx.guild.id) in config.self_assignable_roles:
            config.self_assignable_roles[str(ctx.guild.id)] = [defaultSelfRole]

        if arg == '':
            await ctx.send("No Role Specified")

        else:
            config.self_assignable_roles[str(ctx.guild.id)].append(arg)
            updateSelfRoles()
            await ctx.send("Self assignable role added.")

	#the link command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removesrole(self, ctx, rolename):
        """ - Remove a set self assignable role (admin)"""
        if not str(ctx.guild.id) in config.self_assignable_roles:
            config.self_assignable_roles[str(ctx.guild.id)] = [defaultSelfRole]

        config.self_assignable_roles[str(ctx.guild.id)].remove(rolename)
        await ctx.send("Removed self assignable role.")
        updateSelfRoles()

	#the showlinks command
    @commands.command()
    async def showselfroles(self, ctx):
        """ - Show the list of the self assignable roles in the server """
        if not str(ctx.guild.id) in config.self_assignable_roles:
            config.self_assignable_roles[str(ctx.guild.id)] = [defaultSelfRole]

        if len(config.self_assignable_roles[str(ctx.guild.id)]) > 0:
            await ctx.send(str(config.self_assignable_roles[str(ctx.guild.id)])[1:-1])
        else:
            await ctx.send("No self assignable roles.")


def setup(client):
    client.add_cog(Roles(client))