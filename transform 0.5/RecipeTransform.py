import NLPtool
import IngredRecog


def veg_safe(obj, veg_type):
# check if an ingredient is safe for vegetarian/vegan
    if veg_type!='vegan' and veg_type!='vegetarian':
        return True
    if veg_type in obj.cuisine:
        return True
    if 'meat' in obj.nutri:
        return False
    if veg_type=='vegan' and 'dairy' in obj.nutri:
        return False
    return True
#


def transform(from_ingreds, to_cuisine_name, Knowledge, mute = False):
# Give a valid transformation
    cuisines = Knowledge[2]
    ingred_attr = Knowledge[0]
    frequent = Knowledge[-1]
    out_list = []
    to_cuisine_name = to_cuisine_name.lower()
    for ingred in from_ingreds:
        fromID = NLPtool.uni_rep(ingred)
        # To use the id instead of the actual name,
        # because all ingredients are stored by id in dictionary ingred_attr
        if fromID not in ingred_attr:
            NUTRI = IngredRecog.nutri_guesser(fromID, frequent)
            if NUTRI == None:
                if to_cuisine_name not in ['vegan','vegetarian']:
                    if not mute:
                        print 'Ingredient', ingred, "not identified: left unchanged"
                    out_list.append(ingred)
                else: # leave this ingredient out in case it is non-veg
                    if not mute:
                        print 'Ingredient', ingred, "not identified: left out"
                continue
        else:
            NUTRI = ingred_attr[fromID].nutri
        substitute = 'NOT FOUND'
        min_unique = 10000
        max_nutri_match = 0
        for candID in ingred_attr:
            if to_cuisine_name in ingred_attr[candID].cuisine:
                cand = ingred_attr[candID].name
                if candID in ingred_attr and \
                        NUTRI.intersection(ingred_attr[candID].nutri) != set() and \
                        cand not in out_list:
                    uniqueness = len(ingred_attr[candID].cuisine)
                    # how unique is this ingredient to this cuisine
                    if uniqueness < min_unique:
                        substitute = cand
                        min_unique = uniqueness
                        max_nutri_match = len(NUTRI.intersection(ingred_attr[candID].nutri))
                    elif uniqueness == min_unique:
                        match = len(NUTRI.intersection(ingred_attr[candID].nutri))
                        if match > max_nutri_match:
                            substitue = cand
                            max_nutri_match = match   
        if substitute == 'NOT FOUND':
            if veg_safe(ingred_attr[fromID], to_cuisine_name):
                if not mute:
                    print "Substitute for", ingred, "not found: left unchanged"
                substitute = ingred
            else:
                if not mute:
                    print "Safe substitute for", ingred, "not found: left out"
        else:
            if not mute:
                print ingred, '-->', substitute
        out_list.append(substitute)
    #out_list = list(set(out_list)) # get rid of possible duplicates
    return out_list
#
