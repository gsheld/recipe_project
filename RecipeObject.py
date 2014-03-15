class RecipeObject:
	"""A class to encapsulate a recipe's name and its ingredients"""
	def __init__(self, inputName = None, inputIngredients = []):
    	self.name = inputName
    	self.ingredients = inputIngredients