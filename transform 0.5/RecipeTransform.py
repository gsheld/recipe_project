import NLPtool
import IngredRecog


def transform(from_ingreds, to_cuisine_name, cuisines, ingred_attr, frequent, mute = False):
# Give a valid transformation
    out_list = []
    target_cuisine = cuisines[to_cuisine_name]
    for ingred in from_ingreds:
        fromID = NLPtool.uni_rep(ingred)
        # To use the id instead of the actual name,
        # because all ingredients are stored by id in dictionary ingred_attr
        if fromID not in ingred_attr:
            NUTRI = IngredRecog.nutri_guesser(fromID, frequent)
            if NUTRI == None:
                if not mute:
                    print 'Ingredient', ingred, "not identified: left unchanged"
                out_list.append(ingred)
                continue
        else:
            NUTRI = ingred_attr[fromID].nutri
        substitute = 'NOT FOUND'
        min_unique = 10000
        max_nutri_match = 0
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
                    max_nutri_match = len(NUTRI.intersection(ingred_attr[candID].nutri))
                elif uniqueness == min_unique:
                    match = len(NUTRI.intersection(ingred_attr[candID].nutri))
                    if match > max_nutri_match:
                        substitue = cand
                        max_nutri_match = match
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
