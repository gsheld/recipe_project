import pprint
import NLPtool
import copy
from IngredObj import IngredObj
import RecipeKnowledgeBuilder
import IngredRecog
import RecipeTransform


def whatis(ingred):
    global ingred_attr
    global frequent
    ID = NLPtool.uni_rep(ingred)
    if ID in ingred_attr:
        ingred_attr[ID].print_info()
    else:
        print ingred+':', 'not found in database'
        nutri_set = IngredRecog.nutri_guesser(ID, frequent)
        if nutri_set != None:
            print 'But we guess it might be a kind of', list(nutri_set)
#


#
def common_words(dictionary, frequency_thres):
    # split and count:
    counter = {}
    for key in dictionary:
        words = key.split()
        for word in words:
            if word not in counter:
                counter[word] = 0
            counter[word] += 1
    # Then find the top N:
    top = []
    for word in counter:
        if counter[word] >= frequency_thres:
            top.append(word)
    # Print to file:
    with open('frequent.txt', 'w') as f:
        for word in top:
            f.write(word + '\n')
#


# print the entire knowledge table
def show_table(ingred_attr):
    for ID in ingred_attr:
        ingred_attr[ID].print_info()
        print ''
#


# ENTRY POINT
path = '.\\'     # CHANGE HERE if path for data folders are changed
nutritions = {}
cuisines = {}
ingred_attr = {}
thrown_list = []
frequent = {}
frequent = RecipeKnowledgeBuilder.learn_ingredients(path, ingred_attr, nutritions, cuisines, thrown_list)
common_words(ingred_attr, 10)
#pprint.pprint(frequent)

print RecipeTransform.transform(['pork','lamb','salt','deep south dry rub'], 'french', cuisines, ingred_attr, frequent)
print ''
print RecipeTransform.transform(['skinless, boneless chicken breasts', 'garlic', \
                                    'balsamic vinegar', 'chicken broth', 'mushrooms', \
                                    'all-purpose flour', 'olive oil', 'butter', \
                                    'dried thyme', 'bay leaf'], 'italian', cuisines, ingred_attr, frequent)

