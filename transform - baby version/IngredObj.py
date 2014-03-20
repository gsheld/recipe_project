class IngredObj:
# holds the original name and some associated attributes of an ingredient
    #name
    #nutri
    #cuisine
    def __init__(self, Name):
        self.name = Name
        self.nutri = set()
        self.cuisine = set()
    def print_info(self, tab=''):
        print tab, 'name:     ', self.name
        print tab, 'nutrition:', self.nutri
        print tab, 'cuisine:  ', self.cuisine
