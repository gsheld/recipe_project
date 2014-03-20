import pprint
import NLPtool
import copy
from IngredObj import IngredObj
from collections import defaultdict


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
# Make the diagram of each ingredient and all
# its associated attributes
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
                nutri = nutri_guesser(ID, frequent_sub)
                if nutri == None:
                    thrown_list.append(cuisine_name+': '+ingred)
                    continue
                else:
                    ingred_attr[ID] = IngredObj(ingred)
                    ingred_attr[ID].nutri = nutri
                    #print ingred, '->', nutri
            ingred_attr[ID].cuisine.add(cuisine_name)
#


#
def nutri_for_frequent_ingred(ingred_attr):
    frequent = {}
    freq_set = set()
    with open('concrete.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            frequent[line] = defaultdict(int)
            freq_set.add(line)
    for ID in ingred_attr:
        hit_set = set(ID.split()).intersection(freq_set)
        for word in hit_set:
            nutri_set = ingred_attr[ID].nutri
            for nutri in nutri_set:
                frequent[word][nutri] += 1
    # Decide on the most probable nutrition classification:
    for word in frequent:
        max_count = -1
        count = frequent[word]
        for nutri in count:
            max_count = max(max_count, count[nutri])
        tmp = set()
        for nutri in count:
            if count[nutri] * 2 > max_count:
                tmp.add(nutri)
        frequent[word] = copy.deepcopy(tmp)
    return frequent
#


def load_knowledge_base(path, nutritions, cuisines):
    nutri_names = ['protein', 'spice', 'vegetables','meat','grain','protein','fruit','fats_oils','dairy']
    cuisine_names = ['french', 'indian', 'italian', 'healthy']
    txt2attr_list(path + 'nutrition categories', nutri_names, nutritions)
    #pprint.pprint(nutritions)
    txt2attr_list(path + 'cuisines', cuisine_names, cuisines)
    #pprint.pprint(cuisines)
#


def build_table(ingred_attr, nutritions, cuisines, frequent_sub, thrown_list):
    add_nutrition(nutritions, ingred_attr)
    frequent_sub = nutri_for_frequent_ingred(ingred_attr)
    #pprint.pprint(frequent_sub)
    add_cuisine(cuisines, ingred_attr, frequent_sub, thrown_list)
    print len(ingred_attr), '\n'
    #pprint.pprint(ingred_attr)
#


def learn_ingredients(path, ingred_attr, nutritions, cuisines, frequent_sub, thrown_list):
    load_knowledge_base(path, nutritions, cuisines)
    build_table(ingred_attr, nutritions, cuisines, frequent_sub, thrown_list)
    #pprint.pprint(thrown_list)
#


def naive_transform(from_ingreds, to_cuisine_name, cuisines, ingred_attr, mute = False):
# Give a valid transformation
    out_list = []
    target_cuisine = cuisines[to_cuisine_name]
    for ingred in from_ingreds:
        fromID = NLPtool.uni_rep(ingred)
        # To use the id instead of the actual name,
        # because all ingredients are stored by id in dictionary ingred_attr
        if fromID not in ingred_attr:
            if not mute:
                print 'Ingredient', ingred, "not identified: left unchanged"
            out_list.append(ingred)
        else:
            substitute = 'NOT FOUND'
            min_unique = 10000
            NUTRI = ingred_attr[fromID].nutri
            for cand in target_cuisine:
                candID = NLPtool.uni_rep(cand)
                if candID in ingred_attr and \
                        NUTRI.intersection(ingred_attr[candID].nutri) != set() and \
                        cand not in out_list:
                    uniqueness = len(ingred_attr[candID].cuisine)
                    # how unique is this ingredient to this cuisine
                    if uniqueness < min_unique:
                        substitute = cand
                        min_unique = uniqueness
                        if min_unique==1: break
            if substitute == 'NOT FOUND':
                if not mute:
                    print "Substitue for", ingred, "not found: left unchanged"
                substitute = ingred
            out_list.append(substitute)
            if not mute:
                print ingred, '-->', substitute
    out_list = list(set(out_list)) # get rid of possible duplicates
    return out_list
#


def whatis(ingred):
    global ingred_attr
    ID = NLPtool.uni_rep(ingred)
    if ID in ingred_attr:
        ingred_attr[ID].print_info()
    else:
        print ingred, 'not found in database'
#


def nutri_guesser(ID, frequent_sub):
# guess the nutrition property of an ID base on the occurance
    for word in frequent_sub:
        if ID.find(word) >= 0:
            return copy.deepcopy(frequent_sub[word])
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
frequent_sub = {}
learn_ingredients(path, ingred_attr, nutritions, cuisines, frequent_sub, thrown_list)
common_words(ingred_attr, 10)


print naive_transform(['pork','lamb','salt','deep south dry rub'], 'french', cuisines, ingred_attr)
print ''
print naive_transform(['skinless, boneless chicken breasts', 'garlic', \
                        'balsamic vinegar', 'chicken broth', 'mushrooms', \
                        'all-purpose flour', 'olive oil', 'butter', \
                        'dried thyme', 'bay leaf'], 'french', cuisines, ingred_attr)

