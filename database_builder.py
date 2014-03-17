from selenium import webdriver
from RecipeObject import RecipeObject
import cPickle

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script
urlFile = open('/text_files/recipe_urls.txt','r')
output = open('database.pkl', 'wb')
database = []

def save():
	cPickle.dump(database, output)
	browser.close()
	urlFile.close()

import atexit
atexit.register(save)

for url in urlFile:
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