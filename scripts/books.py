#!/usr/bin/env python3

import os
import re
import datetime
import pandas as pd
import in_place
import csv




# class Book(bookFilteredDataFrame, book):
# 	"""Take a unique Book in a pd.DataFrame and perform stats fill for attributes like 'currentPage', etc."""
# 	def __init__(self, name, totalPages, currenPage):
# 		self.name = book
		
def getBooksNames(booksDataFrame):
	books_names = booksDataFrame.name.unique()
	return books_names

def getBookDataFrame(booksDataFrame:pd.DataFrame, book:str):
	book = booksDataFrame.loc[booksDataFrame.name == book, :]
	return book


def getBookStats(bookDataFrame):
	stats = {}

	name = bookDataFrame.name.unique()
	if len(name) > 1:
		raise ValueError('Was expected to DataFrame have only one unique book name')
	else:
		name = name[0]
		stats.setdefault('name', name)


	totalPages = bookDataFrame.totalPages.unique()
	if len(totalPages) > 1:
		raise ValueError('Was expected to DataFrame have only one value of "totalPages"')
	else:
		totalPages = totalPages[0]
		stats.setdefault('totalPages', totalPages)

	currentPage = bookDataFrame.currentPage.max()
	stats.setdefault('currentPage', currentPage)

	return stats

def printBookStats(bookStats:dict):
	print()
	print(f" {bookStats['name']} ".center(70, '='))
	print(f"· totalPages:\t{bookStats['totalPages']}")
	print(f"· currentPage:\t{bookStats['currentPage']}")
	print()

def askCurrentPage(bookDataFrame):
	print('Do you made progress in this book? [y/N]')
	while True:
		answ = input('> ').strip().lower()
		if answ not in ['y', 'n', '']:
			print('Please, type only:\n"Y" for "YES"\n"N" for "NO"\n(Note: empty input will be considered as "NO"\n')
		else:
			break
	if answ in ['n', '']:
		print("Okay, I won't update this book for now")
	else:
		print('In which page are you currently in?')
		while True:
			page = input('> ').strip().lower()

			if not page.isnumeric():
				print(f'Please, type only a integer number.\n{page} is {type(page)}')
			else:
				page = int(page)
				break
		return page

def performBooksFileUpdate(bookDataFrame, currentPage, books_file):
	pd.options.mode.chained_assignment = None
	rowToUpdate = bookDataFrame.iloc[-1]
	rowToUpdate.currentPage = currentPage
	rowToUpdate = list(rowToUpdate)
	# rowToUpdate.append('\n')
	with open(books_file, 'a', newline='') as books:
		b = csv.writer(books, lineterminator='\n')
		b.writerow(rowToUpdate)

def performBookUpdateMarkdown(bookDataFrame):
	pass

def mainBooks(books_file):
	
	booksDataFrame = pd.read_csv(books_file)
	books_names = getBooksNames(booksDataFrame)
	
	for book in books_names[0:1]:
		# TODO: Get unique book DataFrame
		bookDataFrame =  getBookDataFrame(booksDataFrame, book)
		# TODO: show book stats
		bookStats = getBookStats(bookDataFrame)
		printBookStats(bookStats)

		# TODO: ask current page
		# currentPage = askCurrentPage(bookDataFrame)

		# TODO: ask if want to corret some info

		# TODO: show aproximatly time remaining
		# TODO: perform update in log file
		currentPage = 10
		performBooksFileUpdate(bookDataFrame, currentPage, books_file)
		
		# if currentPage:
		# 	print('+'*70)
		# 	performBookUpdateDataFrame(bookDataFrame, currentPage)


if __name__ == '__main__':

	# TODO: remove `books_file` from here, and catch tthis info parsing `sys.arg` or something similar
	books_file = os.path.join('..', 'data', 'books_logs.csv')
	mainBooks(books_file)