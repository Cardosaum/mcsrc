#!/usr/bin/env python3
#
# Study Stats make a log of currently studing materials
#

import os
import subprocess
import pickle
import datetime
import csv
import pprint
import pandas as pd

currentBooks = {
				"OpenIntro Statistics": {
											"totalPages": 422,
											"currentPage": 0
										}
				}

booksAdd = (('OpenIntro Statistics', 422), ('R for Data Science', 520), ('HandsOn Programming with R', 247), ('Linear Algebra - Foundations to Frontiers', 469))

def inputInt(text):
	""" 
	Validate user input
	"""

	while True:
		try:
			userInput = int(input(text))
			break
		except ValueError:
			print('Please, you need to insert a integer number!')
			print()
	return userInput

def askCurrentPage(book:tuple):
	"""
	User interface function,

	Aks the user for infos and update the log file
	"""

	bookName = book[0]
	bookInfos = book[1]
	print('='*30)
	print(book)
	print(f"· Book: {bookName}")
	print()
	print(f"\tTotal Pages: {bookInfos['totalPages']}")
	print(f"\tCurrent Saved Page: {bookInfos['currentPage']}")
	currentPage = inputInt('In wich page are you right now?\t')
	currentBooks[bookName]["currentPage"] = currentPage
	timeAks = datetime.datetime.now().strftime('%s')
	print(currentBooks)

	infos = []
	infos.append(bookName)
	infos.append(bookInfos["totalPages"])
	infos.append(bookInfos["currentPage"])
	infos.append(timeAks)
	return infos


def saveLog(infos:list):
	"""
	Takes `infos` and save to logs file
	"""
	
	with open(os.path.join('..', 'data', 'books_logs.csv'), 'a') as log:
		w = csv.writer(log)
		w.writerow(infos)


def createBooksInfos(filePath, booksAdd:tuple, fileName='books_infos.csv'):
	""" 
	Creates the first info file
	"""
	file = os.path.join(filePath, fileName)
	booksAttributesHeader = ["name", "totalPages"]
	with open(file, 'w') as f:
		w = csv.writer(f)
		w.writerows([g for g in booksAdd])

def getBooksInfos(fileInfo):
	"""
	This Function read the logs.csv file and return a dictionary with the following contents:

	{

		"Book1": {
			"totalPages": x
			"currentPage": y
		},

		"Book2": {
			"totalPages": w
			"currentPage": z
		}

	}
	"""
	with open(fileInfo, 'r') as f:
		r = list(csv.reader(f))
		pprint.pprint(r)
		d = pd.DataFrame(r)
		print(d.head())
		# TODO: use pandas to select current page (the highest `currentPage` number for each book)



getBooksInfos(os.path.join('..', 'data', 'books_logs.csv'))

# g = askCurrentPage(list(currentBooks.items())[0])

# print(f'\n\n{g}')

# saveLog(g)


# createBooksInfos(os.path.join('..', 'data'), booksAdd=booksAdd)