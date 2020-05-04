import discord
from discord.ext import commands

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

import re
import os
from os import path

#the greetings cog class
class Mtsac(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#the classes command - used to access information about any class at mt sac
	@commands.command()
	async def classes(self, ctx, *args):
		""" - Gets classes information at Mt. SAC"""
		term = args[0]
		subj = args[1].upper()
		if len(args) == 3:
			courseNum = args[2]
		else:
			courseNum = ""
		
		os.chdir(os.path.dirname(os.path.realpath(__file__)))
		#operning the appropriate using the term form to fill and submit
		o = "https://mountiediscordbot.netlify.app/classes/" + term + ".html?subj=" + subj
		if courseNum != "":
			o += ("&num=" + courseNum) 

		#opening the form that will open the classes page
		browser.get(o)

		#waiting until we are redirected to the classes page
		wait = WebDriverWait(browser, 10)
		wait.until(lambda browser: browser.current_url == "https://prodssb.mtsac.edu/prod/bwckschd.p_get_crse_unsec")

		#selecting all the elements with information about the classes
		qr = browser.find_elements_by_css_selector(".pagebodydiv > .datadisplaytable > tbody > tr")
		
		#dictionary to see if a course number has been seen before
		classesDict = { }


		try:
			os.mkdir("temp")
		except:
			pass

		os.chdir("temp")
		
		#looping through the rows in the page
		for elem in qr:
			#checking if the row is a title
			if "ddtitle" in elem.find_element_by_css_selector("*").get_attribute('class').split():
				#getting the course text from the page
				course = elem.find_element_by_css_selector("a").get_attribute('innerHTML')
				#finding the course number using regex
				if courseNum != "":
					cnum = courseNum
				else:
					cnum = re.findall("\\b\\d{3}\\b|\\b\\d{2}\\b|\\b\\d[A-Za-z]\\b|\\b\\d\\b" , course)[0]
				
				if not cnum in classesDict:
					classesDict[cnum] = True
					await ctx.send("Showing Classes for Subject: " + subj + " " + cnum)
					
				await ctx.send("CRN: " + re.findall("\\b[0-9]{5}\\b" , course)[0])
				
			#checking if the row is class information
			elif "dddefault" in elem.find_element_by_css_selector("*").get_attribute('class').split():
				filename = "image.png"
				
				#getting a screenshot of the element and sending it
				elem.screenshot(filename)
				await ctx.send(file=discord.File(filename))
				os.remove(filename)
				
		os.chdir("../")
		os.rmdir("temp")

def setup(client):
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	if path.exists("resources/geckodriver.exe"):
		global browser
		options = Options()
		#making browser headless
		options.headless = True

		browser = webdriver.Firefox(options=options, executable_path=r'resources\geckodriver.exe')
		client.add_cog(Mtsac(client))