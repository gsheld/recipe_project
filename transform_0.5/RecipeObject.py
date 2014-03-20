class RecipeObject:
	"""A class to encapsulate a recipe's name and its ingredients"""
	def __init__(self, inputName = None, inputIngredients = [], url = None):
		self.name = inputName
		self.url = url
		self.ingredients = inputIngredients