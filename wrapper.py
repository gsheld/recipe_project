import subprocess, sys, os
from selenium import webdriver

def mainMenu():
	print '\nWhat would you like to do?\n'
	print '1:  TRANSFORM A RECIPE'
	print '2:  FUN SEARCH - PART 2'
	print '3:  EXIT\n'

	return raw_input('>> ')

def transformRecipe():
	url = raw_input('Enter the URL of the recipe you would like to transform:\n>> ')
	# Logic for transformation #
	#
	#
	#
	runProgram()

def funSearch():
	searchTerm = raw_input('Enter the ingredient you\'re curious about:\n>> ')
	# Logic for fun search #
	#
	#
	#
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
		os._exit(0)

	else:
		print 'Please enter a valid input.'
		runProgram()

runProgram()