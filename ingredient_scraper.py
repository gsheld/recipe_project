# NOTE: Try-except is necessary because the pages are partially loaded through JS and selenium may not wait until a
# page is finished loading before attempting to find elements.

from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script

ingredientMap = {}
ingredientDB_1 = 'http://www.food.com/library/all.zsp'
ingredientDB_2 = 'http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView#recipes'
file = open('ingredients.txt', 'w')

# Pulling from ingredientDB_1 #
browser.get(ingredientDB_1)
links = browser.find_elements_by_xpath('//div[@class="content"]/ul/li')
for item in links:
	current = item.text.lower()
	if not ingredientMap.has_key(current):
		ingredientMap[current] = True
		file.write(current.encode('utf8'))
		file.write('\n')


#Pulling from ingredientDB_2 #
browser.get(ingredientDB_2)
recipeLinks = []
currentLink = ingredientDB_2

for i in range(0,100):
	recipeXPath = '//div[@class="searchResult hub-list-view"]/div[@class="search_mostPop"]/div[@class="searchRtSd"]/h3/a'
	recipes = browser.find_elements_by_xpath(recipeXPath)
	nextLink = browser.find_elements_by_partial_link_text('NEXT ')

	while True:
		try:
			for item in recipes:
				recipeLinks.append(item.get_attribute("href"))
		except Exception:
			browser.get(currentLink)
			recipes = browser.find_elements_by_xpath(recipeXPath)
			continue
		break

	while True:
		try:
			if len(nextLink) > 0:
				time.sleep(1.5)
				currentLink = nextLink[0].get_attribute("href")
				browser.get(currentLink)
		except Exception:
			browser.get(currentLink)
			continue
		break

for item in recipeLinks:
	browser.get(item)
	elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')

	while True:
		try:
			for element in elements:
				current = element.text.lower()
				if not ingredientMap.has_key(current):
					ingredientMap[current] = True
					file.write(current.encode('utf8'))
					file.write('\n')
		except Exception:
			elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')
			continue
		break

browser.close()

file.close()