import string
import pprint

# Read the lists for all the attribute names passed in
# folder    = path
# attr_name = file name & attribute name 
def read_attribute_list(folder, attr_names, Dict):
    for attr_name in attr_names:
        tmp = []
        filename = folder + '\\' + attr_name + '.txt'
        with open(filename, 'r') as f:
            for line in f:
                tmp.append(line.lower().rstrip())
        Dict[attr_name] = tmp
#


# Make the diagram of each ingredient and all
# its associated attributes
def add_ingredient_attributes(attr2ingred, ingred2attr, isNuitri = False):
    for attr in attr2ingred:
        for ingred in attr2ingred[attr]:
            if ingred not in ingred2attr:
                ingred2attr[ingred] = {}
                if isNuitri:
                    ingred2attr[ingred]['NUITRI'] = []
            ingred2attr[ingred][attr] = True
            if isNuitri:
                ingred2attr[ingred]['NUITRI'].append(attr)
#


# Give a valid transformation
def naive_transform(from_ingreds, to_cuisine_name, all_cuisines, ingred_attr):
    out_list = []
    target_cuisine = all_cuisines[to_cuisine_name]
    for ingred in from_ingreds:
        ##print ingred##
        if ingred not in ingred_attr or 'NUITRI' not in ingred_attr[ingred]:
            print 'Ingredient', ingred, "not identified: left unchanged"
            out_list.append(ingred)
        else:
            substitute = 'NOT FOUND'
            nuitri = ingred_attr[ingred]['NUITRI'][0]
            for cand in target_cuisine:
                ##print cand##
                if cand in ingred_attr and \
                        'NUITRI' in ingred_attr[cand] and\
                        nuitri in ingred_attr[cand]['NUITRI'] and \
                        cand not in out_list:
                    substitute = cand
                    break
            if substitute == 'NOT FOUND':
                print "Substitue for", ingred, "not found: left unchanged"
                substitute = ingred
            out_list.append(substitute)
    return out_list
#


# Entry point
def main():
    # Load knowledge
    nuitri_names = ['protein', 'spice', 'vegetable']
    cuisine_names = ['veg','nonveg']
    nuitritions = {}
    cuisines = {}
    read_attribute_list('nuitrition categories', nuitri_names, nuitritions)
    #pprint.pprint(nuitrition)
    read_attribute_list('cuisines', cuisine_names, cuisines)
    #pprint.pprint(cuisines)
    # compile ingredient attributes
    ingred_attr = {}
    add_ingredient_attributes(nuitritions, ingred_attr, True)
    add_ingredient_attributes(cuisines, ingred_attr)
    #pprint.pprint(ingred_attr)
    print naive_transform(['beef','lamb','salt','curry powder'], 'veg', cuisines, ingred_attr)
#


main()
