
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import re
import sys
import string
import json
import random
from itertools import cycle
from pprint import pprint
from nltk.util import ngrams
from nltk.util import trigrams
from nltk.util import bigrams

def getRecipeInfo():

	### Here the webpage with the recipe is opened ###

	myURL = sys.argv[1]	#'http://allrecipes.com/Recipe/Beef-Brisket-My-Way/'
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
		fullSingleIngredient = str(value.get_attribute("innerHTML"))
		if string.find(fullSingleIngredient, ', ') > -1:
			singleIngredientParts = string.split(fullSingleIngredient, ', ')
			singleIngredient['name'] = singleIngredientParts[0]
			singleIngredient['descriptor'] = singleIngredientParts[1]
		else:
			singleIngredient['name'] = fullSingleIngredient
			singleIngredient['descriptor'] = ''
		singleIngredient['preparation'] = ''
		ingredients.append(singleIngredient)
		singleIngredient = {}
	i = 0
	for value in ingredientSet1AmountsObjects:
		amount = str(value.get_attribute("innerHTML"))
		qty = re.search(r"[a-z]+", amount)
		if qty != None:
			#print qty.group(0)
			ingredients[i]['measurement'] = qty.group(0)
			myQty = string.replace(amount, str(qty.group(0)), '')
			myQty = myQty.strip()
			if string.find(myQty, '/') > -1:			
				qtyNum = string.split(myQty, '/')
				if string.find(qtyNum[0], ' ') > -1:
					numerator = string.split(qtyNum[0], ' ')
					ingredients[i]['quantity'] = (float(numerator[0])*float(qtyNum[1])+float(numerator[1]))/float(qtyNum[1])
				else:
					ingredients[i]['quantity'] = float(qtyNum[0])/float(qtyNum[1])
			else:
				ingredients[i]['quantity'] = myQty
		else:
			ingredients[i]['measurement'] = 'unit'
			ingredients[i]['quantity'] = float(str(value.get_attribute("innerHTML")))
		i += 1

	ingredientSet2NamesXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap secondColumn"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngName"]'
	ingredientSet2NamesObjects = driver.find_elements_by_xpath(ingredientSet2NamesXPath)

	ingredientSet2AmountsXPath = '//div[@class="ingred-left"]/ul[@class="ingredient-wrap secondColumn"]/li[@id="liIngredient"]/label/p[@class="fl-ing"]/span[@id="lblIngAmount"]'
	ingredientSet2AmountsObjects = driver.find_elements_by_xpath(ingredientSet2AmountsXPath)

	for value in ingredientSet2NamesObjects:
		fullSingleIngredient = str(value.get_attribute("innerHTML"))
		if string.find(fullSingleIngredient, ', ') > -1:
			singleIngredientParts = string.split(fullSingleIngredient, ', ')
			singleIngredient['name'] = singleIngredientParts[0]
			singleIngredient['descriptor'] = singleIngredientParts[1]
		else:
			singleIngredient['name'] = fullSingleIngredient
			singleIngredient['descriptor'] = ''
		singleIngredient['preparation'] = ''
		ingredients.append(singleIngredient)
		singleIngredient = {}

	for value in ingredientSet2AmountsObjects:
		amount = str(value.get_attribute("innerHTML"))
		qty = re.search(r"[a-z]+", amount)
		if qty != None:
			#print qty.group(0)
			ingredients[i]['measurement'] = qty.group(0)
			myQty = string.replace(amount, str(qty.group(0)), '')
			myQty = myQty.strip()
			if string.find(myQty, '/') > -1:			
				qtyNum = string.split(myQty, '/')
				if string.find(qtyNum[0], ' ') > -1:
					numerator = string.split(qtyNum[0], ' ')
					ingredients[i]['quantity'] = (float(numerator[0])*float(qtyNum[1])+float(numerator[1]))/float(qtyNum[1])
				else:
					ingredients[i]['quantity'] = float(qtyNum[0])/float(qtyNum[1])
			else:
				ingredients[i]['quantity'] = myQty
		else:
			ingredients[i]['measurement'] = 'unit'
			ingredients[i]['quantity'] = float(str(value.get_attribute("innerHTML")))
		i += 1

	#pprint(ingredients)

	directions = []
	i = 0
	directionsXPath = '//div[@class="directLeft"]/ol/li/span'
	directionsObjects = driver.find_elements_by_xpath(directionsXPath)

	for value in directionsObjects:
		directions.append(str(value.get_attribute("innerHTML")))
		i += 1
	#print directions

	driver.quit()
	cookingMethods = {}
	with open('/Users/arundhatijaswal/Documents/Q2/NLP/recipes/recipe_project/text_files/cookingMethods.txt', 'r') as f:
		for line in f:
			cookingMethods[string.replace(line, '\n', '').strip()] = True
	#pprint(cookingMethods)
	cookingUtensils = {}
	with open('/Users/arundhatijaswal/Documents/Q2/NLP/recipes/recipe_project/text_files/cookingUtensils.txt', 'r') as f:
		for line in f:
			cookingUtensils[string.replace(line, '\n', '').strip()] = True
	#pprint(cookingUtensils)
	recipeCookingMethods = []
	recipeCookingUtensils = []

	localPhrase = ''
	for step in directions:
		for phrase in ngrams(string.split(step), 4):
			for word in phrase:
				localPhrase += word
				localPhrase += ' '
			localPhrase = localPhrase.strip()
			localPhrase = localPhrase.replace(',', '')
			localPhrase = localPhrase.replace('.', '')
			for tool in cookingUtensils.keys():
				if tool.lower() == localPhrase.lower():
					#print localToolPhrase, 'utensil ->', tool
					recipeCookingUtensils.append(tool)
			localPhrase = ''
		#print '4-grams done'
		for phrase in trigrams(string.split(step)):
			for word in phrase:
				localPhrase += word
				localPhrase += ' '
			localPhrase = localPhrase.strip()
			localPhrase = localPhrase.replace(',', '')
			localPhrase = localPhrase.replace('.', '')
			for tool in cookingUtensils.keys():
				if tool.lower() == localPhrase.lower():
					#print localToolPhrase, 'utensil ->', tool
					#flag = 1
					#for myTool in recipeCookingUtensils:
					#	if string.find(myTool, localPhrase) > -1:
					#		flag = 0
					#if flag == 1:
					recipeCookingUtensils.append(tool)
			for method in cookingMethods.keys():
				if method.lower() == localPhrase.lower():
					recipeCookingMethods.append(method)
			localPhrase = ''
		#print '3-grams done'
		for phrase in bigrams(string.split(step)):
			for word in phrase:
				localPhrase += word
				localPhrase += ' '
			localPhrase = localPhrase.strip()
			localPhrase = localPhrase.replace(',', '')
			localPhrase = localPhrase.replace('.', '')
			for tool in cookingUtensils.keys():
				if tool.lower() == localPhrase.lower():
					#print localPhrase, 'utensil ->', tool
					#flag = 1
					#for myTool in recipeCookingUtensils:
					#	if string.find(myTool, localPhrase) > -1:
					#		flag = 0
					#if flag == 1:
					recipeCookingUtensils.append(tool)
			for method in cookingMethods.keys():
				if method.lower() == localPhrase.lower():
					#flag = 1
					#for myMethod in recipeCookingMethods:
					#	if string.find(myMethod, localPhrase) > -1:
					#		flag = 0
					#if flag == 1:
					recipeCookingMethods.append(method)
			localPhrase = ''
		for word in string.split(step, ' '):
			#print word
			if len(word) > 2:
				word = word.replace(',', '')
				word = word.replace('.', '')
				for method in cookingMethods.keys():
					#if string.find(method, word) > -1:
					if method.lower() == word.lower():
						#flag = 1
						#for myMethod in recipeCookingMethods:
						#	if string.find(myMethod, localPhrase) > -1:
						#		flag = 0
						#if flag == 1:
						recipeCookingMethods.append(method)
				for tool in cookingUtensils.keys():
					#if string.find(tool, word) > -1:
					if tool.lower() == word.lower():
						#print localPhrase, 'utensil ->', tool
						#flag = 1
						#for myTool in recipeCookingUtensils:
						#	if string.find(myTool, localPhrase) > -1:
						#		flag = 0
						#if flag == 1:
						recipeCookingUtensils.append(tool)
		#print '1-grams done'
	recipe = {}
	recipe['ingredients'] = ingredients
	recipe['cooking method'] = random.choice(recipeCookingMethods)
	recipe['cooking tools'] = recipeCookingUtensils

	pprint(recipe)
	myInternalRecipe = {}
	myInternalRecipe['name'] = str(recipeName)
	myInternalRecipe['ingredients'] = []
	for item in ingredients:
		myInternalRecipe['ingredients'].append(item['name'])
	
	#print myInternalRecipe
	
	f = open('recipeJson.json', 'w')
	jobj = json.dumps(recipe)
	f.write(jobj)
	f.close()
	with open('recipeJson.json', 'r') as f:
		myJobj = map(json.loads, f)
	#print myJobj

	#pg_src = driver.page_source.encode("utf-8")
	#time.sleep(1)
	#driver.quit()

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


