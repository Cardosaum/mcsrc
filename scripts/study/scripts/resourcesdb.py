#!/usr/bin/env python3

#
# Script to handle resources data
#

import json
import pathlib
import collections
import pprint
import pandas as pd

#### Config ####

# Directories
data_path = '../resources_data'

# Files
resources_file = 'resources_properties.json'

# Default Resources Properties
# format: ( `key` , `valueType` )
defaultResourceProps = [
                        ( 'name', str ),
                        ( 'duration', int ),
                        ( 'status', int ),
                        ( 'subject_path', str ),
                        ( 'subject_sequence', int ),
                        ( 'link', str ),
                        ( 'type', str ),
                        ( 'studying_now', bool ),
                        ( 'main_category', str ),
                        ( 'tags', list )
                        ]

# Aesthetics
fillLength = 70

################

# Setup Resources Data
data_path = pathlib.Path(data_path)
resources_file = pathlib.Path.joinpath(data_path, resources_file)
defaultResourceProps = collections.defaultdict(dict, defaultResourceProps)
    

def findType(prop, drp=defaultResourceProps):
        """ This function loop through `defaultResourceProps` and find the type of the given `prop`"""

        for p, t in drp.items():
                if prop == p:
                        return t
        return 'Property not found'

        
def populate():
    """ Function to interactively populate `resources_file` """

    print()
    print(' Executing "Populate" Function '.center(fillLength, '#'))

    while askYN('Add Resource?'):
        addResource(performWrite=True)

    print()
    print(' Creating Config File '.center(fillLength, '#'))

def askYN(text, defaulAnswer='y'):
    """ Ask user to respond either Yes or No """
    yyes = ['y']
    nnoo = ['n']
    if defaulAnswer == 'y':
               yyes.append('')
    elif defaulAnswer == 'n':
               nnoo.append('')
    else:
               raise ValueError('defaulAnswer muste be either "Y" or "N"')
        
    accept = yyes + nnoo


    choices = [ i.upper() if i is defaulAnswer else i for i in accept ]
    choices = [ i for i in choices if i ]
    
    print(text + f' [{"/".join(choices)}]')
    a = input('> ').strip().lower()

    if a not in accept:
        print('Please, you must only insert "Y" for "YES" or "N" for "NO"')
        while True:
            a = input('> ').strip().lower()
            if a in accept:
                break
    if a in yyes:
        return True
    else:
        return False


def answer(name, typeValue):
    """ get user answer """

    str_cancel = '-1'
    answer = None

    while answer == None:
        try:
            if typeValue is not bool:
                answer = typeValue(input(f'· {name.title()} ({typeValue.__qualname__}): \n> ').strip())
            else:
                answer = int(input(f'· {name.title()} ({typeValue.__qualname__}): \n> ').strip())

            print()

            if typeValue is list or typeValue is tuple:
                answer = ''.join(answer)
                answer = answer.split(',')
                answer = [ item.strip() for item in answer ]

            if typeValue is bool:
                if answer == 1:
                    answer = True
                elif answer == 0:
                    answer = False
                elif answer == int(str_cancel):
                    answer = str(answer)
                else:
                    answer = ''

            if answer == '':
                raise ValueError

            if answer == str_cancel:
                answer = ''

        except ValueError:
            print()
            print('Please, you must insert a valid value!')
            print(f'If you want to insert a empty value, insert "{str_cancel}".')
            print(f'Insert a "{typeValue.__qualname__}" type.')

            if typeValue is bool:
                print('Insert:\n\t"0" for "False"\n\t"1" for "True"')

            print()
            answer = None



    return answer

# def inputValid(name, typeValue):

#   str_cancel = '-1'
#   names_bool = ['studying_now']
#   while True:
#       try:

#           answer = answer(name, typeValue)
            
#           if typeValue == list:
#               print('Note: Tags must be comma separated')


#           print()

#           if answer == '' and typeValue == str:
#               print(f'If you want to insert a empty value, insert "{str_cancel}"')
#               continue
#           elif answer == f'{str_cancel}':
#               answer = ''
#       except ValueError:
#           print()
#           print('Please, you must insert a valid value!')
            
#           if name in names_bool:
#               print('Insert:\n\t"0" for "False"\n\t"1" for "True"\n')
#               continue

            
#           if typeValue == int:
#               print(f'If you want to insert a empty value, insert "{str_cancel}"')
            
#           print(f'Insert a "{typeValue.__qualname__}" type.')
#           print()
#           continue

#       if type(answer) == typeValue:
#           break
#   return answer


def writeResources(resourcesDict):
    """ write dict to `resources_file` """

    # write resources content
    with resources_file.open('w') as f:
        json.dump(resourcesDict, f, sort_keys=True, indent=4)


def readResources(resources_file):
    """ Get `resources_file` content as a dict """

    try:
        with resources_file.open() as rf:
            resourcesDict = json.load(rf)

    except json.decoder.JSONDecodeError:
        return

    return resourcesDict






def addKey(key, defaultValue='', resourcesDict=resources_file, performWrite=False):
    """ read `resources_file` and add a common key (`defaltValue`) to all resources listed.
        By default, this function will only return the updated dict, without rewrite `resources_list` """

    resourcesDict = getResourcesDict()

    # loop for ResourcesID and their props
    for rID, p in resourcesDict.items():
        resourcesDict[rID][key] = defaultValue

    if performWrite:
        writeResources(resourcesDict)

    return resourcesDict

# TODO: write function to loop for all resources and ask to edit only one specifc key
#       (or add option to specify wich functions want to edit/add on the fly - through
#        interactive interaction with user. ) similar idea to `askAndCreateDict`


def editKeyvalue(key, value=None, resourceID=None, defaultValue=None, resourcesDict=resources_file, interactive=False, performWrite=False, recusive=False):
    """ function to loop for all resources and edit only one specifc key-value.
        behaviour can be changed by parameters """

    resourcesDict = getResourcesDict()


    # Set logical conditions
    assert resourceID or recusive, f"You must specify either `resourceID` or `recusive` parameter!"
    if interactive:
        assert interactive and value == None, f"If you want `interactive`={interactive} you mustn't specify `value` at all"

    # loop for ResourcesID and their props
    for rID, p in resourcesDict.items():

        # If resourceID was specified, only change one entry
        if resourceID:
            if resourceID == rID:
                resourcesDict[rID][key] = value


        elif recusive:
                        if interactive:
                                print(f' {resourcesDict[rID]["name"]} '.center(fillLength, '='))
                                ans = askYN(f'Do you want to edit key `{key}` ?\nCurrent value is "{resourcesDict[rID][key]}"\n\n', defaulAnswer='n')
                                if ans:
                                        value = answer(f'{key}', findType(key))
                                        resourcesDict[rID][key] = value

                        else:
                            resourcesDict[rID][key] = value


    if performWrite:
        writeResources(resourcesDict)

    return resourcesDict

def getResourcesDict(resourcesDict=resources_file, resourcesIDs=[]):
    """ Read `resources_file` and return their value. Else, return dict passed """


    # Get Resources Content from `resources_file`
    if resourcesDict == resources_file:
        resourcesDict = readResources(resources_file)

    try:
        resourcesDict = collections.defaultdict(dict, resourcesDict)

    except TypeError: 

        resourcesDict = collections.defaultdict(dict)

    if resourcesIDs:

        filtredDict = collections.defaultdict(dict)

        # loop for Resource ID and their respective properties
        for rID, p in resourcesDict.items():
            for requiredItem in resourcesIDs:
                if rID == requiredItem:
                    filtredDict[rID] = p

        return filtredDict
    return resourcesDict


def addResource(resources_file=resources_file, performWrite=False, askUserIfAdd=False):
    """ Function to add one resource to `resources_file` """

    # Get default resource props 
    props = defaultResourceProps

    # Get current resources from `resources_file`
    resourcesDict = getResourcesDict()

    # Ask if user want to insert a entry manualy
    if askUserIfAdd:
        yeah =  askYN('Do you want to insert one more resource?')
        if not yeah:
            return 

    # creat new resource id
    n = getNumberOfResources()
    nrID = f'{(n+1):04d}'
    print()
    print(f' Resource {nrID} '.center(70, '='))
    for name, typeValue in props.items():
        resourcesDict[f'id_{nrID}'][name] = answer(name, typeValue)

    print(''.center(70, '='))
    print()

    if performWrite:
        writeResources(resourcesDict)

    return resourcesDict



def getNumberOfResources(resources_file=resources_file):
    """ parse `resources_file` and get number of insered resources """

    resourcesDict = getResourcesDict()

    # get Number Of ReosurceS
    nors = int(len(resourcesDict.keys()))

    return nors

def getMainCategories(resources_file=resources_file):

    resourcesDict = getResourcesDict()

    # Get Main Categories
    mc = set()

    # for Resource and Properties in ResourceDict
    for r, p in resourcesDict.items():
        for k, v in p.items():
            if k == 'main_category':
                mc.add(v)
    return sorted(mc)

def groupByKey(property, resources_file=resources_file):
    """ loop over dict and return all resources that have same `value` for a given key """

    resourcesDict = getResourcesDict()

    # get a Set Of Resources that have same property
    sor = set()

    for rID, p in resourcesDict.items():
        for k, v in p.items():
            set.add(resourcesDict[rID][k])

# TODO: write function to rename key from resourcesDict

# TODO: write functions to create a Markdown file from contents in `resources_file`

def convertDataFrameToDict(bdf):

    return collections.defaultdict(dict, bdf.T.to_dict())


def getResourcesFrame():
    """ get resources frame """

    rf = pd.DataFrame(getResourcesDict()).T

    return rf

if __name__ == '__main__':
    # getResourcesFrame()
    # categoriesAndValues()
    # populate()
        pprint.pprint(editKeyvalue('subject_path', recusive=True, interactive=True, performWrite=True))
        # answer('this is the name', str)
