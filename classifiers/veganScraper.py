from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Firefox() 

ingredientMap = {}
ingredientDB_1 = 'http://www.mnn.com/food/healthy-eating/stories/vegan-grocery-list-top-50-staples-for-a-meat-free-diet'
file = open('veganadd.txt', 'w')

# Pulling from ingredientDB_1 #
browser.get(ingredientDB_1)
link1 = browser.find_elements_by_xpath('//strong')



for item in link1:
	current = item.text.lower()
	print current

print 'done'

browser.close()

file.close()
