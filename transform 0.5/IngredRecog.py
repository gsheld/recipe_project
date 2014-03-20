import copy
from collections import defaultdict
import NLPtool


def nutri_guesser(ID, frequent):
# guess the nutrition property of an ID base on the occurance
    for word in frequent:
        if ID.find(word) >= 0:
            return copy.deepcopy(frequent[word])
#


#
def nutri_for_frequent_ingred(path, ingred_attr):
    frequent = {}
    freq_set = set()
    with open(path+'concrete.txt', 'r') as f:
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
    #pprint.pprint(frequent)
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
