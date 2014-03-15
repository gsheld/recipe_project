from selenium import webdriver

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script
theFile = open('recipe_urls.txt', 'r+')
urlMap = {}

for line in theFile:
	urlMap[line] = True

ingredientDB = 'http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView&Page='
'#recipes'
recipeLinks = []

for i in range(1,2389):
	browser.get(ingredientDB + str(i) + '#recipes')
	recipeXPath = '//div[@class="searchResult hub-list-view"]/div[@class="search_mostPop"]/div[@class="searchRtSd"]/h3/a'
	recipes = browser.find_elements_by_xpath(recipeXPath)

	while True:
		try:
			for item in recipes:
				itemURL = item.get_attribute("href")
				if not urlMap.has_key(itemURL):
					urlMap[itemURL] = True
					theFile.write('\n')
					theFile.write(itemURL)
		except Exception:
			browser.get(ingredientDB + str(i) + '#recipes')
			recipes = browser.find_elements_by_xpath(recipeXPath)
			continue
		break

browser.close()
theFile.close()