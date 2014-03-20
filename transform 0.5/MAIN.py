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
def show_table():
    global Knowledge
    ingred_attr = Knowledge[0]
    for ID in ingred_attr:
        ingred_attr[ID].print_info()
        print ''
#


# ENTRY POINT
path = '.\\'     # CHANGE HERE if path for data folders are changed
Knowledge = RecipeKnowledgeBuilder.learn_ingredients(path)
# Knowledge: [ingred_attr, nutritions, cuisines, thrown_list, frequent]
common_words(Knowledge[0], 10)
#pprint.pprint(Knowledge[-1])

print RecipeTransform.transform(['pork','lamb','salt','deep south dry rub'], 'french', Knowledge)
print ''
print RecipeTransform.transform(['skinless, boneless chicken breasts', 'garlic', \
                                    'balsamic vinegar', 'chicken broth', 'mushrooms', \
                                    'all-purpose flour', 'olive oil', 'butter', \
                                    'dried thyme', 'bay leaf'], 'healthy', Knowledge)

