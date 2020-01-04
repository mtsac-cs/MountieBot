import discord
import os

from discord.ext import commands

prefix = '!'

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('We have logged in as ' + str(bot.user))


#change cwd to directory of file
os.chdir(os.path.dirname(os.path.realpath(__file__)))


#loading all the cogs from the cogs folder
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension('cogs.'+filename[:-3])


bot.run('***token***')