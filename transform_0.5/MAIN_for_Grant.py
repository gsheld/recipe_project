import pprint
import NLPtool
import copy
from IngredObj import IngredObj
import RecipeKnowledgeBuilder
import IngredRecog
import RecipeTransform


def whatis(ingred):
    global Knowledge
    ingred_attr = Knowledge[0]
    frequent = Knowledge[-1]
    ID = NLPtool.uni_rep(ingred)
    if ID in ingred_attr:
        ingred_attr[ID].print_info()
    else:
        print ingred+':', 'not found in database'
        nutri_set = IngredRecog.nutri_guesser(ID, frequent)
        if nutri_set != None:
            print 'But we guess it might be a kind of', list(nutri_set)
#

# print the entire knowledge table
def show_table():
    global Knowledge
    ingred_attr = Knowledge[0]
    for ID in ingred_attr:
        ingred_attr[ID].print_info()
        print ''
#

def transformMain():
    # ENTRY POINT
    path = './transform_0.5/'     # CHANGE HERE if path for data folders are changed
    Knowledge = RecipeKnowledgeBuilder.learn_ingredients(path)
    # Knowledge: [ingred_attr, nutritions, cuisines, thrown_list, frequent]
    #pprint.pprint(Knowledge[-1])

    print RecipeTransform.transform(['pork','lamb','salt','deep south dry rub'], 'french', Knowledge)
    print ''
    print RecipeTransform.transform(['skinless, boneless chicken breasts', 'garlic', \
                                        'balsamic vinegar', 'chicken broth', 'mushrooms', \
                                        'all-purpose flour', 'olive oil', 'butter', \
                                        'dried thyme', 'bay leaf'], 'healthy', Knowledge)

