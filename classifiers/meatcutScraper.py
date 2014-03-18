# NOTE: Try-except is necessary because the pages are partially loaded through JS and selenium may not wait until a
# page is finished loading before attempting to find elements.

from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Firefox() 

ingredientMap = {}
ingredientDB_1 = 'http://www.mealsforyou.com/cgi-bin/customize?meatcutsveal.html'
file = open('meat.txt', 'w')

# Pulling from ingredientDB_1 #
browser.get(ingredientDB_1)
link1 = browser.find_elements_by_xpath('//b')



for item in link1:
	current = item.text.lower()
	print current

print 'done'

browser.close()

file.close()
