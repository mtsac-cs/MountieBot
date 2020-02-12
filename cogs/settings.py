import sys
import os

import discord
from discord.ext import commands


import pymysql.cursors

import json

#from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import config

#function to update custom prefixes in remote mysql database
def updateCustomPrefixes():
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
                    # Read a single record
                    c_prefixes = json.dumps(config.custom_prefixes, separators=(',', ':'))
                    sql = "UPDATE `prefixes` SET `custom_prefixes` = %s LIMIT 1;"
                    cursor.execute(sql, (c_prefixes))
            finally:
                connection.commit()
                connection.close()
        except:
            print("Failed to update database.")
    

#the greetings cog class
class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the prefix function - to add, remove, or list the prefixes
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *arg):
        """ - add, remove, or list the command prefixes (admin)"""

        guildid = str(ctx.message.guild.id)
        command = arg[0]

        #setting the default prefixes as the prefixes of the guild if this is the first time the prefix command has been used
        if not guildid in config.custom_prefixes:
            config.custom_prefixes[guildid] = config.default_prefixes
            updateCustomPrefixes()
        
        #checking if there are two arguments
        if(len(arg) == 2):

            #the prefix is the second argument
            p = arg[1]

            #making sure the prefix is one character
            if len(p) == 1:

                #to add the prefix
                if command == 'add':
                    if not p == '>':
                        if not p in config.custom_prefixes[guildid]:
                            config.custom_prefixes[guildid].append(p)
                            await ctx.send("Added the prefix " + p)
                            updateCustomPrefixes()
                        else:
                            await ctx.send(p + " is already a prefix")
                    else:
                        await ctx.send(p + " is not a valid prefix")
						
                    
                
                #to remove the prefix
                if command == 'remove':
                    if p in config.custom_prefixes[guildid]:
                        config.custom_prefixes[guildid].remove(p)
                        await ctx.send("Removed the prefix " + p)
                        updateCustomPrefixes()
                    else:
                        await ctx.send("That is not a prefix")
        #if there is only one argument
        else:
            #to list the prefixes
            if command == 'list':
                prefs = str(config.custom_prefixes[guildid])[1:-1] #", ".join(config.custom_prefixes[guildid])
                await ctx.send("Prefixes: " + prefs)


def setup(client):
    client.add_cog(Settings(client))