from RecipeObject import RecipeObject
import cPickle

databaseFile = open('database.pkl', 'rb')
database = cPickle.load(databaseFile)

for recipeItem in database:
	print '***' + recipeItem.name + '***'
	for ingredient in recipeItem.ingredients:
		print ingredient

databaseFile.close()