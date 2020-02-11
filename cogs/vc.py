import discord

from discord.ext import commands
from discord.utils import get
from pytube import YouTube      #need to pip install pytube
from moviepy.editor import *    #need to pip install moviepy

#the roles cog class
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_vc = None
        self.user_vc = None
        self.member = None
        self.server = None


    #the define function will define any word
    @commands.command()
    async def play(self, ctx, url):
        """ - Join current voice channel, plays songs from YouTube (almost there!)"""

        yt = YouTube(url)
        GLOBALPATH = os.getcwd()    #where vids/audio are at

        if GLOBALPATH[0] == '/':
            #MAC PATH
            MUSICPATH = GLOBALPATH + '/Bot Music'
        else:
            #WINDOWS PATH   
            MUSICPATH = GLOBALPATH + '\Bot Music'

        vidTitle = yt.views     #number of views acts as videoID/title
        yt.streams.first().download(MUSICPATH, vidTitle)    #downloads vid to specified path
        vidFileName = vidTitle + ".mp4"
        audioFileName = yt.title + ".mp3"
        video = VideoFileClip(os.path.join(MUSICPATH,vidFileName))      #creates video clip
        video.audio.write_audiofile(os.path.join(MUSICPATH, audioFileName))     #creates audio clip from video clip
        os.remove(os.path.join(MUSICPATH,vidFileName))      #deletes video file

        try:
            self.member = ctx.message.author
            self.server = ctx.message.guild
            self.user_vc = self.member.voice.channel

            if self.bot_vc == self.user_vc:
                await ctx.send("But I'm already here!")

            else:
                if self.user_vc == None:
                    await ctx.send("Please join a Voice Channel first so I know where to go")

                else:
                    await self.user_vc.connect()
                    self.bot_vc = self.user_vc
        
        except discord.errors.ClientException:
            await ctx.send("Sorry, I am currently in the voice channel \"" + self.bot_vc.name + "\"")

        except AttributeError:
            await ctx.send("An error has occured in joining! Please try again")

    @commands.command()
    async def leave(self, ctx, arg = ''):
        """ - Leave current voice channel"""

        self.member = ctx.message.author
        self.server = ctx.message.guild
        self.user_vc = self.member.voice.channel

        if self.bot_vc == self.user_vc and self.bot_vc != None:
            try:
                serverVC = ctx.message.guild.voice_client

                await serverVC.disconnect()
                self.bot_vc = None

            except AttributeError:
                await ctx.send("An error has occured in leaving! Please try again")
        
        else:
            
            if self.bot_vc == None:
                await ctx.send("You can't make me leave a voice channel if I was never in one")
            
            else:
                await ctx.send("You have to be in the same Voice Channel as me for that function to work")

            

def setup(client):
    client.add_cog(Music(client))