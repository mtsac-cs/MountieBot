import discord
from discord.ext import commands

import os
import sys

import pymysql.cursors
import json

import re

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import config


#function to update links in remote mysql database
def updateLinks():
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
					#getting the links dictionary as a string
					g_links = json.dumps(config.links, separators=(',', ':'))
					#updating the database
					sql = "UPDATE `links` SET `guild_links` = %s LIMIT 1;"
					cursor.execute(sql, (g_links))
			finally:
				connection.commit()
				connection.close()
		except:
			print("Failed to update database.")

#the Links cog class
class Link(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	#listening to all message events
	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.author.bot:
			#checking if the link prefix is used
			if(message.content[0] == '>'):
				#sending the url if a link name is sent
				command = message.content[1:].split()[0]
				if str(message.guild.id) in config.links and command in config.links[str(message.guild.id)]:
					await message.channel.send(config.links[str(message.guild.id)][command])

	#the link command
	@commands.command()
	async def link(self, ctx, linkname, result):
		""" - Create a link to a url... send '>linkname' to see the url """
		if not str(ctx.guild.id) in config.links:
				config.links[str(ctx.guild.id)] = {}

		if re.match("^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$", result):
			config.links[str(ctx.guild.id)][linkname] = result
			await ctx.send("Added link.")
			updateLinks()
		else:
			await ctx.send("Invalid url.")

	#the link command
	@commands.command()
	async def unlink(self, ctx, linkname):
		""" - Remove a set link """
		if not str(ctx.guild.id) in config.links:
			config.links[str(ctx.guild.id)] = {}
			
		del config.links[str(ctx.guild.id)][linkname]
		await ctx.send("Removed link.")
		updateLinks()

	#the showlinks command
	@commands.command()
	async def showlinks(self, ctx):
		""" - Show the list of the links in the server """
		if not str(ctx.guild.id) in config.links:
			config.links[str(ctx.guild.id)] = {}

		if len(config.links[str(ctx.guild.id)]) > 0:
			await ctx.send(str(config.links[str(ctx.guild.id)])[1:-1].replace(", ", "\n"))
		else:
			await ctx.send("No links.")

def setup(client):
	client.add_cog(Link(client))