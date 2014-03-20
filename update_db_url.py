from RecipeObject import RecipeObject
import cPickle

databaseFile = open('database.pkl', 'rb')
database = cPickle.load(databaseFile)
urlFile = open('./text_files/recipe_urls.txt','r')
output = open('database-updated.pkl', 'wb')
database_updated = []

count = 0;

for url in urlFile:
	currentRO = database[count]
	currentRO.url = url
	database_updated.append(currentRO)
	count += 1

cPickle.dump(database_updated, output)

databaseFile.close()
urlFile.close()
output.close()