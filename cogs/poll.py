import discord
import threading
import asyncio

from discord.ext import commands
from collections import Counter


#the poll cog class
class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        self.voters = []
        self.options = []
        self.polll = False


    #poll command will run a poll in the chat
    @commands.command()
    async def poll(self, ctx, question, seconds, *ops: str):
        """ - Opens poll in the format !poll "q?" [sec] "options" if multiple words, put in double quotes"""
        self.votes.clear()
        self.voters.clear()
        self.options.clear()
    
        self.polll = True

        #appends all the options listed by user to global options
        for x in range(0, len(ops)):
            self.options.append(ops[x])

        #validation of the poll requirements
        if int(seconds) > 0:
            await ctx.send('Poll started! ' + question + ' Poll ends in ' + seconds + ' seconds')
        elif int(seconds) == 0 or int(seconds) < 0:
            await ctx.send('Cannot have zero or negative seconds for a poll!')

        #checking if there's more than one option and less than 10 options
        if len(ops) <= 1:
            await ctx.send('Need more than one option for a poll!')
            return
        if len(ops) > 10:
            await ctx.send('Cannot have more than 10 options for a poll!')
            return

        #timer of the poll
        async def countdown(t):
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                if t <= 3:
                    await ctx.send(timer)    
                await asyncio.sleep(1)
                t-=1
            await ctx.send('Poll ended.')
            self.polll = False
            cnt = Counter()
            for word in self.votes:
                cnt[word] += 1
            await ctx.send(Counter(self.votes).most_common(2))

        #call countdown after user sets seconds
        t=seconds
        await countdown(int(t))


    @commands.command()
    async def vote(self, ctx, *, val, member: discord.Member = None):
        """ - Send a vote while poll is active"""
        #store voter id in array called voters
        if self.polll == True:
            member = ctx.message.author

            #check if valid option 
            print('before got voters')
            if val not in self.options:
                    await ctx.send('Not a valid option! The options are:')
                    await ctx.send(self.options)
                    return
            else:
                #check if person has voted with the stored member id
                if member not in self.voters:
                    self.voters.append(member)
                    await ctx.send('Recorded.') 

                    #append the vote to vote list  
                    self.votes.append(val)
                    await ctx.send('Thanks for the vote!')         
                else:
                    await ctx.send('Cannot vote more than once!')
                    return
               
        #if there isn't a poll called, send no poll
        elif self.polll == False:
            await ctx.send('No poll happening right now.')
            return


def setup(client):
    client.add_cog(Poll(client))