from selenium import webdriver
from RecipeObject import RecipeObject
import cPickle
import os
import sys

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script
urlFile = open('recipe_urls.txt','r')

databaseFile = open('database.pkl', 'rb')
database = cPickle.load(databaseFile)
databaseFile.close()
os.remove('database.pkl')
output = open('database.pkl', 'wb')

should_I_Start = False

def save():
	cPickle.dump(database, output)
	browser.close()
	urlFile.close()

import atexit
atexit.register(save)

count = 0

for url in urlFile:

	count += 1
	if count == 1442:
		should_I_Start = True

	if not should_I_Start:
		continue

	browser.get(url)

	while True:
		try:
			currentIngredientList = []
			elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')
			titleElement = browser.find_element_by_xpath('//h1[@id="itemTitle"]')
			titleElementText = titleElement.text
		except Exception:
			browser.get(url)
			continue
		break

	while True:
		try:
			for element in elements:
				current = element.text.lower()
				currentIngredientList.append(current)
		except Exception:
			elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')
			continue
		break

	database.append(RecipeObject(titleElementText, currentIngredientList))