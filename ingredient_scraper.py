from selenium import webdriver
import string, cPickle

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script

ingredientMap = {}
ingredientDB_1 = 'http://www.food.com/library/all.zsp'
ingredientDB_2 = 'http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView#recipes'

# Pulling from ingredientDB_1 #
browser.get(ingredientDB_1)
links = browser.find_elements_by_xpath('//div[@class="content"]/ul/li')
for item in links:
	current = item.text.lower()
	if not ingredientMap.has_key(current):
		# print current
		ingredientMap[current] = True


#Pulling from ingredientDB_2 #
canContinue = True
browser.get(ingredientDB_2)
recipeLinks = []

for i in range(0,1):
	recipeXPath = '//div[@class="searchResult hub-list-view"]/div[@class="search_mostPop"]/div[@class="searchRtSd"]/h3/a'
	recipes = browser.find_elements_by_xpath(recipeXPath)
	nextLink = browser.find_elements_by_partial_link_text('NEXT ')

	for item in recipes:
		recipeLinks.append(item.get_attribute("href"))

	if len(nextLink) > 0:
		browser.get(nextLink[0].get_attribute("href"))
	else:
		canContinue = False

for item in recipeLinks:
	browser.get(item)
	elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')

	# Try-except is necessary because the pages are partially loaded through JS and selenium may not wait until a
	# page is finished loading before attempting to find elements.
	try:
		for element in elements:
			current = element.text.lower()
			if not ingredientMap.has_key(current):
				# print current
				ingredientMap[current] = True
	except Exception:
		elements = browser.find_elements_by_xpath('//div[@class="ingred-left"]/ul/li/label/p/span[@class="ingredient-name"]')
		for element in elements:
			current = element.text.lower()
			if not ingredientMap.has_key(current):
				# print current
				ingredientMap[current] = True

browser.close()

file = open('ingredients.txt', 'w')
for key in ingredientMap.keys():
	file.write(key.encode('utf8'))
	file.write('\n')

file.close()