import pprint
import NLPtool
from IngredObj import IngredObj
import IngredRecog


def txt2attr_list(folder, attr_names, Dict):
# Read the lists for all the attribute names passed in
# folder    = path
# attr_name = file name & attribute name 
    for attr_name in attr_names:
        tmp = []
        filename = folder + '\\' + attr_name + '.txt'
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
    nutri_names = ['protein', 'spice', 'vegetables',\
                   'meat', 'grain', 'protein', 'fruit',\
                   'fats_oils', 'dairy', 'condiments']
    cuisine_names = ['french', 'indian', 'italian', \
                     'healthy','chinese', 'vegan', \
                     'vegetarian', 'mexican']
    txt2attr_list(path + 'nutrition categories', nutri_names, nutritions)
    #pprint.pprint(nutritions)
    txt2attr_list(path + 'cuisines', cuisine_names, cuisines)
    #pprint.pprint(cuisines)
#


def build_table(path, ingred_attr, nutritions, cuisines, thrown_list):
    add_nutrition(nutritions, ingred_attr)
    frequent = IngredRecog.nutri_for_frequent_ingred(path, ingred_attr)
    #pprint.pprint(frequent)
    add_cuisine(cuisines, ingred_attr, frequent, thrown_list)
    #print len(ingred_attr), '\n'
    return frequent
#


def learn_ingredients(path):
    nutritions = {}
    cuisines = {}
    ingred_attr = {}
    thrown_list = []
    frequent = {}
    load_knowledge_base(path, nutritions, cuisines)
    frequent = build_table(path, ingred_attr, nutritions, cuisines, thrown_list)
    return [ingred_attr, nutritions, cuisines, thrown_list, frequent]
    #pprint.pprint(thrown_list)
    #pprint.pprint(frequent)
#
