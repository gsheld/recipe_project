import sys
def removeDoubles(filename1, filename2):
    fileIn = open(filename1, 'r')
    fileOut = open(filename2, 'w')
    myMap = []
##    for line in fileIn:
##                if not myMap.has_key(line):
##                    myMap[line] = True
##                    fileOut.write(str(line))

    for line in fileIn:
        myMap.append(str(line).lower())

    nodoubles = list(set(myMap))
    nodoubles.sort()

    for l in nodoubles:
        fileOut.write(l)

    
    fileIn.close()
    fileOut.close()


removeDoubles('italian.txt', 'italian_final.txt')
removeDoubles('french.txt', 'french_final.txt')
removeDoubles('indian.txt', 'indian_final.txt')
removeDoubles('filipino.txt','filipino_final.txt')
removeDoubles('american.txt','american_final.txt')
removeDoubles('chinese.txt','chinese_final.txt')
removeDoubles('mexican.txt','mexican_final.txt')
removeDoubles('vegetarian.txt','vegetarian_final.txt')
removeDoubles('meat.txt','meat_final.txt')
removeDoubles('vegan.txt','vegan_final.txt')
removeDoubles('protein.txt','protein_final.txt')
removeDoubles('grain.txt','grain_final.txt')
removeDoubles('spice.txt','spice_final.txt')
removeDoubles('fats_oils.txt','fats_oils_final.txt')
removeDoubles('dairy.txt','dairy_final.txt')
removeDoubles('vegetables.txt','vegetables_final.txt')
removeDoubles('fruit.txt','fruit_final.txt')
removeDoubles('healthy.txt','healthy_final.txt')
removeDoubles('condiments.txt', 'condiments_final.txt')
print "done"
