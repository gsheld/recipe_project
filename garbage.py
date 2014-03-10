
	### Here we're just cleaning up the data that we've collected ###
	"""
		"""
		#if 'table ' in item and flag == 1:
		#	tablecount += 1
		#	my_iter.next()
			"""
			award_title = my_iter.next()
			if 'href' not in award_title and award_title not in awards:
				awards[award_title] = []
				award_title_key = award_title
				flag = 1
			"""
		elif 'views-field-nominee-name' in item and flag == 1:
			nominee = my_iter.next()
			if len(nominee) > 0:
				awards[award_title_key].append(nominee)
		elif '\"grey' in item and flag == 1:
			nominee = my_iter.next()
			if len(nominee) > 0:
				awards[award_title_key].append(nominee)
		elif '\"gold' in item and flag == 1:
			nominee = my_iter.next()
			if len(nominee) > 0:
				awards[award_title_key].append(nominee)
		elif 'text/javascript' in item and flag == 1:
			break
		else:
			my_iter.next()
		"""
	for key in awards.keys():
		if len(key.strip()) != 0 and len(awards[key]) == 0:
			break
	awards[key] = awards['']
	awards.pop('', None)
	del_keys = [key for key in awards.keys() if '\n' in key]
	for key in del_keys:
		awards.pop(key, None)
	
	### Now we simple output our data on the terminal and write it to a file ###
	
	print 'Golden Globes\n- - - - - -'
	nominee_filename = 'GG' + sys.argv[1] + 'nominees.txt'
	with open(nominee_filename, 'w') as file:
		file.write(str(awards))
	from pprint import pprint
	pprint(awards)
	print '\n- x - x -\n'
	"""
