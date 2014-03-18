
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import re
import sys
import string
from itertools import cycle
from pprint import pprint

def getRecipeInfo():
	
	### Here the webpage with the recipe is opened ###
	
	driver = webdriver.Firefox()
	myURL = 'http://allrecipes.com/Recipe/Slow-Cooker-Corned-Beef-and-Cabbage/'
	print myURL
	driver.get(myURL)
	
	### Here the recipe name is extracted ###
	
	recipeNameXPath = '//div[@class="detail-right fl-right"]/h1[@id="itemTitle"]'
	recipeNameObject = driver.find_elements_by_xpath(recipeNameXPath)
	
	for value in recipeNameObject:
		recipeName = value.get_attribute("innerHTML")
	print recipeName
	
	ingredients = []
	singleIngredient = {}
	ingredientSet1NamesXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngName"]'
	ingredientSet1NamesObjects = driver.find_elements_by_xpath(ingredientSet1NamesXPath)
	
	ingredientSet1AmountsXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngAmount"]'
	ingredientSet1AmountsObjects = driver.find_elements_by_xpath(ingredientSet1AmountsXPath)

	for value in ingredientSet1NamesObjects:
		singleIngredient['name'] = str(value.get_attribute("innerHTML"))
		ingredients.append(singleIngredient)
		singleIngredient = {}
	i = 0
	for value in ingredientSet1AmountsObjects:
		ingredients[i]['quantity'] = str(value.get_attribute("innerHTML"))
		i += 1
	
	ingredientSet2NamesXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap secondColumn"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngName"]'
	ingredientSet2NamesObjects = driver.find_elements_by_xpath(ingredientSet2NamesXPath)
	
	ingredientSet2AmountsXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap secondColumn"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngAmount"]'
	ingredientSet2AmountsObjects = driver.find_elements_by_xpath(ingredientSet2AmountsXPath)

	for value in ingredientSet2NamesObjects:
		singleIngredient['name'] = str(value.get_attribute("innerHTML"))
		ingredients.append(singleIngredient)
		singleIngredient = {}
	
	for value in ingredientSet2AmountsObjects:
		ingredients[i]['quantity'] = str(value.get_attribute("innerHTML"))
		i += 1
	
	#pprint(ingredients)
	
	directions = []
	i = 0
	
	### PROBLEM POINT - DOESN'T FETCH ANYTHING ###
	
	directionsXPath = '//div[@class="directions"]/div[@class="directLeft"]/ol/li/span[@id="plaincharacterwrap break"]'
	directionsObjects = driver.find_elements_by_xpath(directionsXPath)
	
	for value in directionsObjects:
		print value.get_attribute("innerHTML")		### SHOULD CONTAIN COOKING DIRECTIONS
		print 'hello'
		directions[i] = str(value.get_attribute("innerHTML"))
		i += 1
	print directions
	
	### END OF PROBLEM POINT ###
	
	cookingMethods = {}
	with open('/Users/arundhatijaswal/Documents/Q2/NLP/recipes/recipe_project/text_files/cookingMethods.txt', 'r') as f:
		for line in f:
			cookingMethods[string.replace(line, '\n', '')] = True
	#pprint(cookingMethods)
	cookingUtensils = {}
	with open('/Users/arundhatijaswal/Documents/Q2/NLP/recipes/recipe_project/text_files/cookingUtensils.txt', 'r') as f:
		for line in f:
			cookingUtensils[string.replace(line, '\n', '')] = True
	#pprint(cookingUtensils)	
	recipeCookingMethods = []
	recipeCookingUtensils = []
	for step in directions:
		print step
		for word in step:
			#print word
			for method in cookingMethods.keys():
				if string.find(method, word) > -1:
					recipeCookingMethods.append(word)
			for tool in cookingUtensils.keys():
				if string.find(tool, word) > -1:
					recipeCookingUtensils.append(word)
	recipe = {}
	recipe['ingredients'] = ingredients
	recipe['cooking method'] = recipeCookingMethods
	recipe['cooking tools'] = recipeCookingUtensils
	
	pprint(recipe)
	
	#pg_src = driver.page_source.encode("utf-8")
	#time.sleep(1)
	driver.quit()
	
	"""
	### The HTML content (treated as a giant string) is split on the basis of tags < & > ###
	
	collector = re.split('>|<', pg_src)
	my_iter = cycle(collector)
	recipe = {}
	valFlag = -1
	flag = 0
	tablecount = 0
	trcount = 0
	i = 1
	j = 0
	parent = ''
	#for i in range(2):
	my_iter.next()
	
	### Now we cycle through our giant list of strings to find ingredient substitutions ###
	
	for item in collector:
		info = my_iter.next()
		if "colspan" in item:
			flag = 1
			#print item, " ; ", info
		if flag == 1 and "tr" in item:
			#if tablecount == 3:
			trcount += 1
			#print item, " ; ", info
		if trcount == 4:
			flag = 0
			#print 'i before incr = ', i
			temp = item.lstrip()
			if re.match('[A-Z]+', temp) != None:
				parent = temp.split(',')
				#print parent
				#print "\n",
				#raw_input("Press Enter to continue...")
			if re.match('[^0-9]', temp) != None and re.match('[A-Z]+', temp) == None:
				#print "\n", 
				#parent=",parent,'<<'
				if len(parent) > 0:
					if string.find(temp, '\xc2') > -1:
						holder = string.replace(temp, '\xc2', '')
						final = string.replace(holder, '\xa0', '')
						temp = parent[0] + ' ' + final
					else:
						temp = parent[0] + temp
					#re.sub('^\s[a-z]+', ' [a-z]+', temp)
				#print 'updated temp=',temp,'<-'
			if i % 2 == 0 and len(temp) > 0:
				#re.match('\s', item.lstrip()) == None and re.match('[^a-z]', item) != None:
				#print('| ', info, ' |'),
				#sys.stdout.write('| ')
				if not re.match(r'[0-9]', temp):
					if valFlag > 0:
						substitutions[key] = sub
					valFlag = 0
					key = temp
					sub = {}
				elif re.match(r'[0-9]', temp) and valFlag == 0:
					sub['amount'] = temp
					valFlag += 1
				else:
					#possibilities = string.split(temp, ';')
					#for option in possibilities:
					#	if len(option) > 2:
					localKey = 'alternate #' + str(valFlag)
					sub[localKey] = temp
					valFlag += 1
				#sys.stdout.write(temp)
				#sys.stdout.write(' |')
				#print 
				#j += 1
			i += 1
			#print item
				#j = 0
			if "colspan" in item:
				return substitutions
	"""
	

### The main function is just to call the function that does everything and gets the data ###

def main():
	getRecipeInfo()
	

if __name__ == "__main__":
	main()


