from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script
theFile = open('ingredients.txt', 'r+')
ingredientsMap = {}

for line in theFile:
	ingredientsMap[line] = True

# Put logic here for adding to file #
ingredientDB = 'http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView&Page='
'#recipes'
recipeLinks = []

for i in range(200,300):
	browser.get(ingredientDB + str(i) + '#recipes')
	recipeXPath = '//div[@class="searchResult hub-list-view"]/div[@class="search_mostPop"]/div[@class="searchRtSd"]/h3/a'
	recipes = browser.find_elements_by_xpath(recipeXPath)

	while True:
		try:
			for item in recipes:
				recipeLinks.append(item.get_attribute("href"))
		except Exception:
			browser.get(ingredientDB + str(i) + '#recipes')
			recipes = browser.find_elements_by_xpath(recipeXPath)
			continue
		break

for item in recipeLinks:
	browser.get(item)
	elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')

	while True:
		try:
			for element in elements:
				current = element.text.lower()
				if not ingredientsMap.has_key(current):
					ingredientsMap[current] = True
					theFile.write('\n')
					theFile.write(current.encode('utf8'))
		except Exception:
			elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')
			continue
		break

browser.close()
theFile.close()