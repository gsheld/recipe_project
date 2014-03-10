
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

def getSubstitutionInfo():
	
	### Here the webpage with the substitution list is opened to get its the entire HTML ###
	
	driver = webdriver.Firefox()
	myURL = 'http://www.ext.colostate.edu/pubs/foodnut/09329.html'
	print myURL
	driver.get(myURL)
	pg_src = driver.page_source.encode("utf-8")
	time.sleep(1)
	driver.quit()
	
	### The HTML content (treated as a giant string) is split on the basis of tags < & > ###
	
	collector = re.split('>|<', pg_src)
	my_iter = cycle(collector)
	substitutions = {}
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
				print "\n", 
				#parent=",parent,'<<'
				if len(parent) > 0:
					temp = parent[0] + temp 
					#re.sub('^\s[a-z]+', ' [a-z]+', temp)
				#print 'updated temp=',temp,'<-'
			if i % 2 == 0 and len(temp) > 0:
				#re.match('\s', item.lstrip()) == None and re.match('[^a-z]', item) != None:
				#print('| ', info, ' |'),
				sys.stdout.write('| ')
				sys.stdout.write(temp)
				sys.stdout.write(' |')
				#print 
				#j += 1
			i += 1
			#print item
				#j = 0
			if "colspan" in item:
				break
	

### The main function is just to call the function that does everything and gets the data ###

def main():
    getSubstitutionInfo()

if __name__ == "__main__":
    main()


