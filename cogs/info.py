import discord
from discord.ext import commands

#from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
import requests

#dictionary=PyDictionary()

headers_Get = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'DNT': '1',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1'
}

#the greetings cog class
class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#the define function will define any word
	@commands.command()
	async def define(self, ctx, *arg):
		""" - Gives the definition to any word"""
		result = ""
		url = "https://www.google.com/search?q=define+" + '+'.join(arg)
		page = requests.get(url, headers=headers_Get)
		soup = BeautifulSoup(page.text, 'html.parser')
		defnBox = soup.select_one("div[jsname='x3Eknd']")
		defns = soup.select("div[jsname='r5Nvmf']")

		for defn in defns:
			partofspeech = defn.select_one(".pgRvse.vdBwhd")
			defnitions = defn.select("div[data-dobid='dfn']")
			result += partofspeech.find(text=True).upper()+":\n"
			i = 1
			for defnition in defnitions:
				result += "\t"+ str(i) + ".) " +defnition.find(text=True)+"\n"
				i+=1
		
		'''using PyDictionary (not working)
		obj = dictionary.meaning(' '.join(arg))
        #the result
        res = ""

        #iterating through the dictioanry with the meaning and appending to the result string
        for pos in obj:
            res += pos + ":\n"
            for definition in obj[pos]:
                res += "\t" + definition + "\n"
        '''
		
		await ctx.send(result)

	@commands.command()
	async def weather(self, ctx, *place):
		""" - Gives weather for any city"""
		url = "https://www.google.com/search?q=weather+in+" + '+'.join(place)
        
		page = requests.get(url, headers=headers_Get)

		soup = BeautifulSoup(page.text, 'html.parser')
		city = soup.find(id="wob_loc").get_text()
		time = soup.find(id="wob_dts").get_text()
		weatherState = soup.find(id="wob_dc").get_text()
		temp = soup.find(id='wob_tm').get_text()
		precip = soup.find(id='wob_pp').get_text()
		humid = soup.find(id='wob_hm').get_text()
		wind = soup.find(id='wob_ws').get_text()

		await ctx.send("Weather in " + city + "\n" + time + "\n" + weatherState + "\n" + "->Temperature: "+ temp + "°F \n" + "->Precipitation: " + precip + "\n" + "->Humidity: " + humid + "\n" + "->Wind: " + wind + "\n")

def setup(client):
    client.add_cog(Info(client))