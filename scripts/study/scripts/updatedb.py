#!/usr/bin/env python3

from pprint import pprint
import pathlib
import resourcesdb


def getbdf():
    return resourcesdb.getResourcesFrame()

def getStudyingBooks(bdf):
    """ return data frame for books that are currently beeing study """

    # get currently studying books
    csb = bdf[(bdf.studying_now == True)]

    return csb

def printBookStatus(bookDF):
    """ return string of current book stats """

    totalPages = bookDF.loc['duration']
    currentPage = bookDF.loc['status']
    name = bookDF.loc['name']

    print()
    print(f" {name} ".center(70, '='))
    print(f"· totalPages:\t{totalPages}")
    print(f"· currentPage:\t{currentPage}")
    print()

def askCurrentPage(bookDF):
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

            if not page.lstrip('-').isnumeric():
                print()
                print(f'Please, type only a integer number.\n"{page}" is {type(page)}')
                print()
                print(f'If you want to cancel this update for book {bookDF.loc["name"]}\nYou need to insert "-1"')
                print()

            elif int(page) == -1:
                print("Okay, I'll assume you does not made any progress for now")
                return None

            elif int(page) <= bookDF.loc['status']:
                print()
                print('Are you sure you made progress?')
                print(f'Current page is {bookDF.loc["status"]}, but you inserted {page}')
                print(f'Please, insert a value greather than {bookDF.loc["status"]}')
                print()
                print(f'If you want to cancel this update for book {bookDF.loc["name"]}\nYou need to insert "-1"')
                print()
            else:
                page = int(page)
                break
        return page

def book(bookDF, bdf):
    printBookStatus(bookDF)
    page = askCurrentPage(bookDF)
    curPage = bookDF.loc['status']
    performUpdate = False
    if page and page > curPage:
        bdf.at[bookDF.name, 'status'] = page
        performUpdate = True

    elif page and page < curPage:
        raise ValueError('Variable `page` is not greather than `curPage`')

    if performUpdate:
        bdf = resourcesdb.convertDataFrameToDict(bdf)
        resourcesdb.writeResources(bdf)


### Setting global variables ###

# Get book data frame
bdf = getbdf()

# get currently studying books
csb = getStudyingBooks(bdf)


################################


if __name__ == '__main__':

    for i in range(len(csb)):
        bookDF = csb.iloc[i]
        book(bookDF, bdf)