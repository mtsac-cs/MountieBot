import discord
from discord.ext import commands
#These modules are requried to use selenium:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import the asyncio module
import asyncio

#This file will contain code for Daniel; AI chat-Bot

#the greetings cog class
class daniel(commands.Cog):
    
    

    def __init__(self, bot):
        self.bot = bot
        self.browser = webdriver.Firefox()
        #create a class variable to check is a web browser is already in use for Selenium
        #This will initially be set to false
        #create an instace of the webdriver that will be used, in this case im using the word "browser", any would work:
        #Note that driver(S) are needed for the specified web browser in order for
        #selenium to work; in this case im using my Firefox Browser with geckoDriver in my computer paths
        self.is_browser_open = False

    @commands.command()
    #This"StartChat" cammand will open a brwoser to cleverbot to start chatting
    async def start_chat(self, ctx):
       # print("In start chat")
        '''-use this first to start a chat with DANIEL '''
        #use an if statement to check if "is_browser_open" is flase
        #if so, start up a browser
        if self.is_browser_open is False:
        
            #print("timeout")
            #set a timeout to stop the program if the webpage does not load
            self.browser.set_page_load_timeout(20)

            #add a wait, in seconds,  for every method used to give the webpage time to load up after each element usage
            self.browser.implicitly_wait(3)
            # print("get url")
            #Go to a specific webpage; in this case "cleverbot":
            self.browser.get("https://www.cleverbot.com/?0")

            #set the class variable to True
            self.is_browser_open = True

            await ctx.send("Daniel has been summoned")
        else:
            #let users know that the convo was already started
            await ctx.send("A conversation was already started")

    @commands.command()
    #this cammand will close the browser; end chat
    async def end_chat(self, ctx):
        #print("in endchat")
        '''-Use this to end the conversation with DANIEL '''
        if self.is_browser_open is True:
            #CLose the browser
            self.browser.quit()

            #set the class boolean to false to indicate a closed convo
            self.is_browser_open = False

            await ctx.send("Conversation over")
        else:
           await ctx.send("A conversation was never started")


    @commands.command()
    #This "chat" cammand will be used to continually converse with daniel
    async def chat(self, ctx, *, User_input):
        #print("in chat")
        ''' -Enter a phrase to chat with DANIEL!'''
        if self.is_browser_open is True:

            #the following will check if the logo "Cleverbot" is in the website, if not then print the message "website not ... websigge":
            assert self.browser.find_element_by_id("cleverbotlogo"), "Website not found or wrong website?"

            #Find the input text box of the website and create an instance of it:
            #in this case i choose to use the word "text_box"
            #this name can be found by right clicking on the text box and select "inspect element"
            #The name of the element of the cleverbot website text box happens to be the word "stimulus"
            text_box = self.browser.find_element_by_name("stimulus")

            #Clear the text_box first using "clear " method:
            text_box.clear()
            #send the "User_input" to the text_box using the "send_keys" method:
            text_box.send_keys(User_input)
            #send the "Enter" or "RETURN" key from keyboard useing the "send_keys" method
            text_box.send_keys(Keys.RETURN)
            
            #Wait for a bit; if this wait is not here, the cleverbot website will not loadup 
            #the response fast enough to web-scrape it and send it to discord.
            await asyncio.sleep(6)

            #Create an instance for the responce that cleverbot gives:
            #i choose the word "response" for my object:
            #using "Inspect elements", the id of cleverbot's response is "line1"
            #additionally, use ".text" method to get the text and store it into "response"
            response = self.browser.find_element_by_id('line1').text
            
            #print the "response" onto the discord chat useing ".send" method:
            await ctx.send("Daniel: " + response)


        else:
           await ctx.send("A convo was never started")

        




 


def setup(client):
    client.add_cog(daniel(client))