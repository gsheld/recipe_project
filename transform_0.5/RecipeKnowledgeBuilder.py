import pprint
import NLPtool
from IngredObj import IngredObj
import IngredRecog
import RecipeProject


def txt2attr_list(folder, attr_names, Dict):
# Read the lists for all the attribute names passed in
# folder    = path
# attr_name = file name & attribute name 
    for attr_name in attr_names:
        tmp = []
        filename = folder + '/' + attr_name + '.txt'
        with open(filename, 'r') as f:
            for line in f:
                ingreds = line.split('/')
                # some ingredients are separated by '/'
                for ingred in ingreds:
                    tmp.append(ingred.lower().rstrip().lstrip())
        Dict[attr_name] = tmp
#
    


def add_nutrition(nutritions, ingred_attr):
# Reorganize nutrition lists by ingredients
    for nutri_name in nutritions:
        nutrition = nutritions[nutri_name]
        for ingred in nutrition:
            ID = NLPtool.uni_rep(ingred)
            # Make unique identifier to merge similar 
            # representations of the same ingredient
            if ID not in ingred_attr:
                ingred_attr[ID] = IngredObj(ingred) # Point ID to a new ingredient object, with name ingred
            ingred_attr[ID].nutri.add(nutri_name)
#


def add_cuisine(cuisines, ingred_attr, frequent_sub, thrown_list):
#Reorganize cuisine lists by ingredients
    for cuisine_name in cuisines:
        cuisine = cuisines[cuisine_name]
        for ingred in cuisine:
            ID = NLPtool.uni_rep(ingred)
            # Make unique identifier to merge similar 
            # representations of the same ingredient
            nutri = None
            if ID not in ingred_attr:
                nutri = IngredRecog.nutri_guesser(ID, frequent_sub)
                if nutri == None:
                    thrown_list.append(cuisine_name+': '+ingred)
                    continue
                else:
                    ingred_attr[ID] = IngredObj(ingred)
                    ingred_attr[ID].nutri = nutri
                    #print ingred, '->', nutri
            ingred_attr[ID].cuisine.add(cuisine_name)
#


def load_knowledge_base(path, nutritions, cuisines):
# Read from file to category lists
    nutri_names = ['protein', 'spice', 'vegetables',\
                   'meat', 'grain', 'protein', 'fruit',\
                   'fats_oils', 'dairy', 'condiments']
    cuisine_names = ['french', 'indian', 'italian', \
                     'healthy','chinese', 'vegan', \
                     'vegetarian', 'mexican']
    txt2attr_list(path + 'nutrition_categories', nutri_names, nutritions)
    #pprint.pprint(nutritions)
    txt2attr_list(path + 'cuisines', cuisine_names, cuisines)
    #pprint.pprint(cuisines)
#


def additional_logic(ingred_attr):
# further complete the nutrition information by following rules:
# * vegan --> vegetarian
# * vegetables --> vegetarian
# * fruit --> vegetarian
# * meat --> protein
    for ID in ingred_attr:
        obj = ingred_attr[ID]
        if 'meat' in obj.nutri:
            obj.nutri.add('protein')
        if 'vegetables' in obj.nutri or \
               'fruit' in obj.nutri or\
               'vegan' in obj.cuisine:
            obj.cuisine.add('vegetarian')
        
#

def build_table(path, ingred_attr, nutritions, cuisines, thrown_list):
# build the table by ingredient from the category lists
    add_nutrition(nutritions, ingred_attr)
    frequent = IngredRecog.nutri_for_frequent_ingred(path, ingred_attr)
    #pprint.pprint(frequent)
    add_cuisine(cuisines, ingred_attr, frequent, thrown_list)
    additional_logic(ingred_attr)
    #print len(ingred_attr), '\n'
    return frequent
#


def load_recipes():
# load the recipe list in the 

def learn_ingredients(path):
# Wrap the entire data table loading and building process
    nutritions = {}
    cuisines = {}
    ingred_attr = {}
    thrown_list = []
    frequent = {}
    load_knowledge_base(path, nutritions, cuisines)
    frequent = build_table(path, ingred_attr, nutritions, cuisines, thrown_list)
    recipes = load_recipes()
    return [ingred_attr, nutritions, cuisines, thrown_list, frequent]
    #pprint.pprint(thrown_list)
    #pprint.pprint(frequent)
#
