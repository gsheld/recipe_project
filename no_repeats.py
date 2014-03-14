import sys

arguments = sys.argv # Command line arguments
file = open(arguments[1], 'r')
 # = open(arguments[1] + '1', 'w')
myMap = {}

for line in file:
	if not myMap.has_key(line):
		myMap[line] = True;
