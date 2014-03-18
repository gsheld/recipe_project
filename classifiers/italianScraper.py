# NOTE: Try-except is necessary because the pages are partially loaded through JS and selenium may not wait until a
# page is finished loading before attempting to find elements.

from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Firefox() 

ingredientMap = {}
ingredientDB_1 = 'http://www.nonnalinaskitchen.com/tools/glossary.htm'
file = open('../italian.txt', 'w')

# Pulling from ingredientDB_1 #
browser.get(ingredientDB_1)
links = browser.find_elements_by_xpath('//b')
for item in links:
	current = item.text.lower()
	if not ingredientMap.has_key(current):
		ingredientMap[current] = True
		file.write(current.encode('utf8'))
		file.write('\n')




browser.close()

file.close()
