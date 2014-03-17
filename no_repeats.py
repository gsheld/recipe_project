# This will remove any repeats in whatever lists you've created. Enjoy!

import sys

arguments = sys.argv # Command line arguments
fileIn = open(arguments[1], 'r')
fileOut = open(arguments[2], 'w')
myMap = {}

for line in fileIn:
	if not myMap.has_key(line):
		myMap[line] = True
		fileOut.write(str(line) + '\n')

fileIn.close()
fileOut.close()