import discord
import os
from os import path

from discord.ext import commands

import config

bot = commands.Bot(command_prefix=config.determine_prefix)

#change cwd to directory of file
os.chdir(os.path.dirname(os.path.realpath(__file__)))


#loading all the cogs from the cogs folder
for filename in os.listdir('cogs'):
    if filename.endswith('.py') and not filename[:-3] in config.optionalCogs:
        bot.load_extension('cogs.'+filename[:-3])

@bot.event
async def on_ready():
    print('We have logged in as ' + str(bot.user))


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, cog):
	""" - Load any extension (admin)"""
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	if path.exists("cogs/"+cog+".py"):
		prelen = len(bot.commands)
		
		bot.load_extension('cogs.'+cog)

		#checking if the extension loaded
		if len(bot.commands) > prelen:
			await ctx.send('Loaded extension.')
		else:
			await ctx.send('Failed to load extension.')
	else:
		await ctx.send('No such extension.')


#bot.add_command(load)


bot.run('***Token**')