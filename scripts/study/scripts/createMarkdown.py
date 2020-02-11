#!/usr/bin/env python3

#
# Script to create markdown from resources data
#


#### Config ####

# Directories
data_path = '../resources_data'

# Files
markdown_file = 'studyCurriculum.md'

# Aesthetics
fillLength = 70

################



import pathlib
import datetime
import pprint
import resourcesdb
import collections

# Setup global variables
data_path = pathlib.Path(data_path)
markdown_file = pathlib.Path.joinpath(data_path, markdown_file)


# Create File

def createFile(content, markdown_file=markdown_file):
    with markdown_file.open('w') as f:
        for line in content:
            f.write(line)


# Create header

def header(markdown_file=markdown_file):
    """ Create File Header """

    updateTime = datetime.datetime.now().strftime('%X, %x')
    header = f"""<h3 align="center">Derived from Open Source Society University
  <br>
  <br>
  <a href="https://github.com/open-source-society/data-science">
    <img alt="Open Source Society University - Data Science" src="https://img.shields.io/badge/OSSU-data--science-blue.svg"></h3>
  </a>
<p align="center">
  :bar_chart: Path to a free self-taught education in <strong>Data Science</strong>!
  <br><br>

</p>

> Last Update: {updateTime}

"""

    return header


# table of contents

def tableOfContents(title='Table of Contents', markdown_file=markdown_file):
    """ Create File Table Of Contents """

    # get Table Of Contents raw data
    toc = resourcesdb.getMainCategories()

    content = ''

    content += addStr(f'## {title}')
    content += addStr('')

    # for Topic in toc
    for t in toc:
        content += addStr(f"- [{t.title()}](#{t.lower().replace(' ', '-')})")

    content.strip()

    return f"\n\n{content}"

def addStr(text:str):
    return (text + '\n')

# print(header())


# TODO: current year block

# TODO: courses on the road map block

def roadMap():
    """ create text to place in `roadmap` section """

    ## Get all `Main Categories`

    # get `resources Frame`
    rf = resourcesdb.getResourcesFrame()

    # get `main categories`
    mc = rf.main_category.unique()
    mc.sort()

    # get list of dataframes containing all resources that belong to one specific
    # `main_category` and is not currently beeing study
    tables = []
    for c in mc:
        a = rf[(rf.main_category == c) & (rf.studying_now == False)]
        if a.empty:
            continue
        tables.append(a)

    # transform each dataframe in defautlt dict
    props = []
    for i in tables:
        a = i.T.to_dict()
        a = collections.defaultdict(dict, a)
        props.append(a)

    # Create text for road map
    text = ''
    for i in props:
        cat = (i[list(i.keys())[0]]['main_category'])
        text += tableHeader(textBefore=f"\n### {cat}\n\n")
        text += tableRow(i)
        text += '\n\n'
    
    text = '## Courses on the Rodmap\n' + text
    return text





def tableCurrentlyStudying():
    """ Create table with resources currently beeing study """

    # Get resources currently beeing study
    rcs = collections.defaultdict(dict)

    for rID, p in resourcesdb.getResourcesDict().items():
        if p['studying_now']:
            rcs[rID] = p


    return tableRow(rcs)


def tableRow(resource, collunmsFromDict=['name', 'duration', 'status'], collunmsCustom=['percentage']):
    """ Create row for table, including specific resource's properties """

    # variables to replace
    # nan_value = '-hamba'

    # Get a list of all collunms
    collunms = collunmsFromDict + collunmsCustom

    # Get string for current row in markdown table
    table = ''
    table_divisor = '| '

    # For ResourceID and respective Property in `resources` dict
    for rID, p in resource.items():
        for col in collunms:

            # Handle some exceptions
            if int(p['duration']) < 0:
                p['duration'] = 0


            # create custom collunms values
            if col == 'percentage':
                try:
                    p['percentage'] = f"{(( p['status'] / p['duration'] ) * 100):.02f}%"
                except ZeroDivisionError:
                    p['percentage'] = '0.00%'


    # write final string for this row
    for rID, p in resource.items():
        for col in collunms:
            if col == 'name':

                typeResource = p['type']
                symbolResource = ''

                if typeResource == 'mooc':
                    symbolResource = ':globe_with_meridians:'
                elif typeResource == 'book':
                    symbolResource = ':book:'

                table += f"{symbolResource} [{str(p[col])}]({str(p['link'])}) {table_divisor}"

            else:
                table += f"{str(p[col])} {table_divisor}"
        table = table.strip(' |')
        table += '\n'

    table = table.strip(' |\n')


    return table

def tableHeader(textBefore='', textAfter=''):
    header = ''
    align = ''

    header += 'Courses | Duration | Status | Percentage'
    align += ':-- | :--: | :--: | :--:'

    final = f"{textBefore}{header}\n{align}{textAfter}"

    return final



# pprint.pprint(resourcesdb.getResourcesDict())
# pprint.pprint(resourcesdb.getResourcesDict(resourcesIDs=['id_0036', 'id_0023']))
# print(resourcesdb.getResourcesDict(resourcesIDs=['id_0036']))
# tableRow(resourcesdb.getResourcesDict(resourcesIDs=['id_0001']))
# print(tableRow(resourcesdb.getResourcesDict(resourcesIDs=['id_0036'])))
# print(tableHeader())


# print(header())
# print(tableHeader(textBefore='## Currently Studying\n\n'))
# print(tableCurrentlyStudying())
# print(tableOfContents())

def markdownPage():

    text = ''

    text += header()
    text += tableOfContents()
    text += f"\n---\n\n"
    text += tableHeader(textBefore='## Currently Studying\n\n')
    text += tableCurrentlyStudying()
    text += f"\n---\n\n"
    text += roadMap()

    return text

print(markdownPage())
createFile(markdownPage())