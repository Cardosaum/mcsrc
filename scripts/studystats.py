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
import re
import in_place

currentBooks = {
				"OpenIntro Statistics": {
											"totalPages": 422,
											"currentPage": 0
										},
				"R for Data Science": {
											"totalPages": 520,
											"currentPage": 40
				},
				"HandsOn Programming with R": {
											"totalPages": 247,
											"currentPage": 0
				},
				"Linear Algebra - Foundations to Frontiers": {
											"totalPages": 469,
											"currentPage": 39
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

def askCurrentPageAllBooks(book:pd.DataFrame='x'):
	"""
	User interface function,

	Aks the user for infos and update the log file
	"""
	dataBooks = pd.read_csv(os.path.join('..', 'data', 'books_data.csv'))
	for row in dataBooks.:
		print(row)

askCurrentPageAllBooks()


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


def updatePathWay(file):
	""" 
	Parse `file`, found corresponding books that are beeing read currently and update status
	example file parsed: https://github.com/Cardosaum/bioinformatics_pathway/blob/master/mcs_self_paced.md
	"""
	# TODO: make this function work and replace `booksInfos` to use the returned value 
	# booksInfos = getBooksInfos(fileInfo)
	booksInfos = currentBooks

	for name, infos in currentBooks.items():
		# print(name, infos)


		with in_place.InPlace(file, backup_ext=".bak") as f:

			# Regex to find lines that correspond to book `name`
			nRe = re.compile(name)

			for line in f:
				nMo = nRe.search(line)

				# if line contain book `name`:
				if nMo:

					# we need to skip lines that contain status for book.
					# see layout of file beeing parsed: https://github.com/Cardosaum/bioinformatics_pathway/blob/master/mcs_self_paced.md

					statusFile = re.compile(r'\sOK')
					sfMo = statusFile.search(line)
					if not sfMo:
						# print(name, infos)
						# print(line)

						# Group 1 of this regex retur the current page
						updateCurrentPageRe = re.compile(r'''
															\/week\s*\| # capture /week 
															\s*(\d+)      # capture  <digits>
															\s*pages?\s*\|   # capture page OR pages
															\s*([\d.])+%+\s* # capture percentage
														''', re.VERBOSE)
						updateCurrentPageMo = updateCurrentPageRe.search(line)
						# print('-'*20)
						# print(updateCurrentPageRe.sub(f'''/week | {str(infos["currentPage"])} pages''', line))

						# Calculate percentage of progress
						try:
							# print(infos)
							# print(updateCurrentPageMo)
							calculatePercent = (infos["currentPage"]/infos["totalPages"])*100
						except ZeroDivisionError:
							calculatePercent = 0
						line = updateCurrentPageRe.sub(f'''/week | {str(infos["currentPage"])} pages | {float(calculatePercent):.2f}%\n''', line) 
						# print('='*20)

				# performs write action
				f.write(line)


# updatePathWay('/home/matheus/mcs/study/bioinformatics_pathway/mcs_self_paced.md')

# getBooksInfos(os.path.join('..', 'data', 'books_logs.csv'))

# g = askCurrentPage(list(currentBooks.items())[0])

# print(f'\n\n{g}')

# saveLog(g)


# createBooksInfos(os.path.join('..', 'data'), booksAdd=booksAdd)