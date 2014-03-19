from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import string, time

browser = webdriver.Firefox() 

def getFood(url, pages, txtfile):
    offset = 0
    counter = 0
    file = open(txtfile, 'w')
    for page in range(0,pages):
        ingredientDB = url + str(offset)
        browser.get(ingredientDB)
        food = browser.find_elements_by_xpath('//div[@class="wbox"]/table/tbody/tr/td/a[@title="Click to view reports for this food"]')
        for item in food:
            current = item.get_attribute("innerHTML")
            current = current.lower()
            if counter:
                file.write(current.encode('utf8'))
                file.write('\n')
            counter = (counter + 1)%2
        offset += 25
    file.close()
    
#Dairy Egg Products#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Dairy+and+Egg+Products&man=&lfacet=&qlookup=&offset=', 11, 'Dairy.txt')
#Spices and Herbs#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Spices+and+Herbs&man=&lfacet=&qlookup=&offset=', 3, 'Spice.txt')
#Fats and Oils#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Fats+and+Oils&man=&lfacet=&qlookup=&offset=', 11, 'Fat_Oils.txt')
#Vegetables and Vegetable Products#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Vegetables+and+Vegetable+Products&man=&lfacet=&qlookup=&offset=',34, 'Vegetables.txt')
#Fruits and Fruit Juices#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Fruits+and+Fruit+Juices&man=&lfacet=&qlookup=&offset=', 14, 'Fruit.txt')
#Cereal Grains and Pasta#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Cereal+Grains+and+Pasta&man=&lfacet=&qlookup=&offset=', 8, 'Grain.txt')
#Finfish and Shellfish Products#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Finfish+and+Shellfish+Products&man=&lfacet=&qlookup=&offset=', 11, 'Seafood.txt')
#Beef Products# #Meat1.txt#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Beef+Products&man=&lfacet=&qlookup=&offset=', 35, 'Meat1.txt')
#Lamb, Veal, and Game Products# #Meat2.txt#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Lamb%2C+Veal%2C+and+Game+Products&man=&lfacet=&qlookup=&offset=', 15, 'Meat2.txt')
#Pork Products# #Meat3.txt#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Pork+Products&man=&lfacet=&qlookup=&offset=', 14, 'Meat3.txt')
#Poultry Products# #Meat4.txt#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Poultry+Products&man=&lfacet=&qlookup=&offset=', 16, 'Meat4.txt')
#Sausages and Luncheon Meats# #Meat5.txt#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Sausages+and+Luncheon+Meats&man=&lfacet=&qlookup=&offset=', 10, 'Meat5.txt')
#Sweets# #KidMeals1.txg#
getFood('http://ndb.nal.usda.gov/ndb/search/list?format=&count=&max=25&sort=&fg=Sweets&man=&lfacet=&qlookup=&offset=', 14, 'KidMeals.txt')

browser.close()
print "DONE!!"


