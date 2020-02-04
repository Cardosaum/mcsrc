#!/usr/bin/env python3

import os
import re
import datetime
import pandas as pd
import in_place
import csv




# class Book(books_file, books_markdown, book):
# 	"""Take a unique Book in a pd.DataFrame and perform stats fill for attributes like 'currentPage', etc."""
# 	def __init__(self):
# 		self.booksDataFrame = pd.read_csv(books_file)
# 		self.books_names = getBooksNames(booksDataFrame)
# 		self.name = self.book
# 		self.booksDataFrame = getBookDataFrame(booksDataFrame, book)
		
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
		# check if page is greater than currentPage (Maybe user inserted wrong value?)
		currentPage = getBookStats(bookDataFrame)['currentPage']
		if page <= currentPage:
			print('Are you sure you made progress in this book?')
			print(f'· Current Page: {currentPage}')
			print(f'· Your input: {page}')
			print()
			print('Do you realy want to update with your input page?')
			print(f'Your progress will be: `{currentPage} - {page} = {currentPage-page}`')
			print('Proceed? [y/N]')
			while True:
				proceed = input('> ').strip().lower()
				if proceed not in ['y', 'n', '']:
					print('Please, type only:\n"Y" for "YES"\n"N" for "NO"\n(Note: empty input will be considered as "NO"\n')
				elif proceed in ['n', '']:
					print(f"Okay, I'll disconsider your input ({page}), and mantain {currentPage}")
					break
				else:
					print('Okay, I\'ll update with your input')
					break
					return page
		else:
			return page

def performBooksFileUpdate(bookDataFrame, currentPage, books_file):
	pd.options.mode.chained_assignment = None
	rowToUpdate = bookDataFrame.iloc[-1]
	rowToUpdate.currentPage = currentPage
	rowToUpdate.time = datetime.datetime.now().strftime('%s')
	rowToUpdate = list(rowToUpdate)
	with open(books_file, 'a', newline='') as books:
		b = csv.writer(books, lineterminator='\n')
		b.writerow(rowToUpdate)

def performBookUpdateMarkdown(bookDataFrame, books_markdown, book, bookStats):
	with in_place.InPlace(books_markdown, backup_ext='.bak') as f:
	# Regex to find lines that correspond to book `name`
		nRe = re.compile(book)

		for line in f:
			nMo = nRe.search(line)

			# if line contain book `name`:
			if nMo:

				# we need to skip lines that contain status for book.
				# see layout of file beeing parsed: https://github.com/Cardosaum/bioinformatics_pathway/blob/master/mcs_self_paced.md

				statusFile = re.compile(r'\sOK')
				sfMo = statusFile.search(line)
				if not sfMo:
					# print(book)
					# print(line)
					# print()

					# Group 1 of this regex return the current page
					updateCurrentPageRe = re.compile(r'''
														\/week\s*\| # capture /week 
														\s*(\d+)      # capture  <digits>
														\s*pages?\s*\|   # capture page OR pages
														\s*([\d.])+%+\s* # capture percentage
													''', re.VERBOSE)
					updateCurrentPageMo = updateCurrentPageRe.search(line)
					# print('-'*20)
					# print(updateCurrentPageRe.sub(f'''/week | {str(bookStats['currentPage'])} pages''', line))

					# Calculate percentage of progress
					try:
						# print(infos)
						# print(updateCurrentPageMo)
						calculatePercent = (bookStats["currentPage"]/bookStats["totalPages"])*100
					except ZeroDivisionError:
						calculatePercent = 0
					# print(updateCurrentPageRe.sub(f'''/week | {str(bookStats["currentPage"])} pages | {float(calculatePercent):.2f}%\n''', line))
					line = updateCurrentPageRe.sub(f'''/week | {str(bookStats["currentPage"])} pages | {float(calculatePercent):.2f}%\n''', line) 
					# print('='*20)

			# Performs write action
			f.write(line)

def getAllData(books_file):
	booksDataFrame = pd.read_csv(books_file)
	books_names = getBooksNames(booksDataFrame)

def mainBooks(books_file, books_markdown):
	
	booksDataFrame = pd.read_csv(books_file)
	books_names = getBooksNames(booksDataFrame)
	
	for book in books_names:
		# TODO: Get unique book DataFrame
		bookDataFrame =  getBookDataFrame(booksDataFrame, book)
		# TODO: show book stats
		bookStats = getBookStats(bookDataFrame)
		printBookStats(bookStats)

		# TODO: ask current page
		currentPage = askCurrentPage(bookDataFrame)

		# TODO: ask if want to corret some info

		# TODO: show aproximatly time remaining
		# TODO: perform update in log file
		if currentPage:
			performBooksFileUpdate(bookDataFrame, currentPage, books_file)
			booksDataFrame = pd.read_csv(books_file)
			bookDataFrame =  getBookDataFrame(booksDataFrame, book)
			bookStats = getBookStats(bookDataFrame)
			performBookUpdateMarkdown(bookDataFrame, books_markdown, book, bookStats)
			print('log file updated'.upper().center(50, '+'))


if __name__ == '__main__':

	# TODO: remove `books_file` from here, and catch tthis info parsing `sys.arg` or something similar
	books_file = os.path.join('..', 'data', 'books_logs.csv')
	books_markdown = os.path.join('..', '..', '..', '..', 'bioinformatics_pathway', 'mcs_self_paced.md')
	mainBooks(books_file, books_markdown)