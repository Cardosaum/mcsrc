#!/usr/bin/env python3

#
# mps.py stands for `Monitoring Progress in Study`
#

import json
import pathlib
import collections
import pprint

#### Config ####

# Directories
data_path = '../data'

# Files
resources_file = 'resources_properties.json'

################

# Setup Resources Data

data_path = pathlib.Path(data_path)
resources_file = pathlib.Path.joinpath(data_path, resources_file)
	

def askAndCreateDict():
	""" Function to interactively populate the first `resources_file` """

	# Aks if want to contine inserting books
	rd = collections.defaultdict(dict)
	n = 1
	props = [('name', str), ('duration', int), ('status', int), ('link', str), ('type', str), ('studying_now', int)]
	while askYN('Do you want to insert one more resource?'):
		nFormated = f'{n:04d}'
		print()
		print(f' Resource {nFormated} '.center(70, '='))
		for name, typeValue in props:
			rd[f'id_{nFormated}'][name] = inputValid(name, typeValue)
			print()

		print(''.center(70, '='))
		print()
		n += 1

	print()
	print(' Creating Config File '.center(70, '+'))
	with open(resources_file, 'a') as f:
		json.dump(rd, f, sort_keys=True, indent=4)

def askYN(text):
	""" Ask user to respond either Yes or No """
	print(text + ' [Y/n]')
	accept = ['y', 'n', '']	
	a = input('> ').strip().lower()

	if a not in accept:
		print('Please, you must only insert "Y" for "YES" or "N" for "NO"')
		while True:
			a = input('> ').strip().lower()
			if a in accept:
				break
	if a == 'y' or a == '':
		return True
	else:
		return False

def inputValid(name, typeValue):

	str_cancel = '-1'
	names_bool = ['studying_now']
	while True:
		try:
			if name in names_bool:
				answer = typeValue(input(f'· {name.title()} ({typeValue.__qualname__}): \n> ').strip())
				if answer == 0:
					answer = False
				elif answer == 1:
					answer = True
				else:
					ValueError
				break


			answer = typeValue(input(f'· {name.title()} ({typeValue.__qualname__}): \n> ').strip())
			print()
			if answer == '' and typeValue == str:
				print(f'If you want to insert a empty value, insert "{str_cancel}"')
				continue
			elif answer == f'{str_cancel}':
				answer = ''
		except ValueError:
			print()
			print('Please, you must insert a valid value!')
			
			if name in names_bool:
				print('Insert:\n\t"0" for "False"\n\t"1" for "True"')
				continue

			
			if typeValue == int:
				print(f'If you want to insert a empty value, insert "{str_cancel}"')
			
			print(f'Insert a "{typeValue.__qualname__}" type.')
			print()
			continue

		if type(answer) == typeValue:
			break
	return answer


def writeResources(resourcesDict):
	""" write dict to `resources_file` """

	# write resources content
	with resources_file.open('w') as f:
		json.dump(resourcesDict, f, sort_keys=True, indent=4)


def readResources(resources_file):
	""" Get `resources_file` content as a dict """

	with resources_file.open() as rf:
		resourcesDict = json.load(rf)

	return resourcesDict




# TODO: write functions to create a Markdown file from contents in `resources_file`


def addKey(addKey, defaultValue='', resourcesDict=resources_file, performWrite=False):
	""" read `resources_file` and add a common key (`defaltValue`) to all resources listed.
		By default, this function will only return the updated dict, without rewrite `resources_list` """

	# Get Resources Content from `resources_file`
	if resourcesDict == resources_file:
		resourcesDict = readResources(resources_file)

	# loop for ResourcesID and their props
	for rID, p in resourcesDict.items():
		resourcesDict[rID][addKey] = defaultValue

	if performWrite:
		writeResources(resourcesDict)

	return resourcesDict

# TODO: write function to loop for all resources and ask to edit only one specifc key
# 		(or add option to specify wich functions want to edit/add on the fly - through
#		 interactive interaction with user. ) similar idea to `askAndCreateDict`