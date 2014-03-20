import subprocess, sys, os, time, json
from selenium import webdriver
from recipeScraper import getRecipeInfo

sys.path.append('./transform_0.5')
from MAIN_for_Grant import transformMain, whatis

def mainMenu():
	print '\nWhat would you like to do?'
	print '1:  TRANSFORM A RECIPE'
	print '2:  FUN SEARCH - PART 2'
	print '3:  PRINT JSON'
	print '4:  EXIT\n'

	return raw_input('>> ')

def transformRecipe():
	internal = None
	complete = None
	transformOptions = {}
	transformOptions['1'] = 'healthy'
	transformOptions['2'] = 'vegetarian'
	transformOptions['3'] = 'vegan'
	transformOptions['4'] = 'chinese'
	transformOptions['5'] = 'filipino'
	transformOptions['6'] = 'french'
	transformOptions['7'] = 'indian'
	transformOptions['8'] = 'italian'
	transformOptions['9'] = 'mexican'
	transformWanted = '1'
	url = raw_input('Enter the URL of the recipe you would like to transform:\n>> ')
	print '\nTransforms possible:'
	for key, value in transformOptions.items():
		print key, ' - ', value
	transformWanted = raw_input('Enter the transform of the recipe you would like to perform:\n>> ')

#	try:
	internal, complete = getRecipeInfo(url)
	#	transformWanted = raw_input('Enter the transform of the recipe you would like to perform:\n>> ')
#	except:
#		print '\n*** Enter a valid allrecipes.com URL ***\n'
#		transformRecipe()

	transformMain(internal['ingredients'], transformOptions[transformWanted])

	raw_input('\nPress Any Key to Continue...')
	runProgram()

def funSearch():
	searchTerm = raw_input('Enter the ingredient you\'re curious about:\n>> ')
	whatis(searchTerm)

	raw_input('\nPress Any Key to Continue...')
	runProgram()

def returnJSON():
	internal = None
	complete = None

	print '\nNote: Our program creates the JSON file in our directory,'
	print '      which you may use for automated grading\n'
	print 'Here we are reading and printing from that JSON file\n'
	url = raw_input('Enter the URL of the recipe you would like to transform:\n>> ')

	try:
		internal, complete = getRecipeInfo(url)
	except:
		print '\n*** Enter a valid allrecipes.com URL ***\n'
		returnJSON()

	with open('recipeJson.json', 'r') as f:
		myJobj = map(json.loads, f)
	print myJobj

	raw_input('\nPress Any Key to Continue...')
	runProgram()

def runProgram():
	subprocess.call(['clear'])
	print '------------------------------------------------------'
	print 'Recipe Transformer - where all your dreams come true!'
	print '------------------------------------------------------'

	userChoice = mainMenu()

	if userChoice == '1':
		transformRecipe()

	elif userChoice == '2':
		funSearch()

	elif userChoice == '3':
		returnJSON()

	elif userChoice == '4':
		os._exit(0)

	else:
		print '\nInvalid input, try again....'
		time.sleep(1)
		runProgram()

runProgram()