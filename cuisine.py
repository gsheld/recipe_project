from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Chrome('./chromedriver') # Make sure chromedriver is in same directory as this script
file = open('cuisines.txt', 'r+')
cuisineMap = {}

for line in file:
	cuisineMap[line] = True

# Put logic here for adding to file #
source_1 = 'http://cafeworld.wikia.com/wiki/List_of_Cuisines'
browser.get(source_1)
moreCuisines = browser.find_elements_by_partial_link_text('Cuisine')

for cuisine in moreCuisines:
	if not cuisineMap.has_key(cuisine):
		file.write('\n')
		file.write(cuisine.text.encode('utf8'))
		cuisineMap[cuisine] = True

browser.close()
file.close()