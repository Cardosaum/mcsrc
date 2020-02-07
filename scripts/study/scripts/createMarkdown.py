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



import json
import pathlib
import collections
import pprint
import resourcesdb

# Setup global variables
data_path = pathlib.Path(data_path)
markdown_file = pathlib.Path.joinpath(data_path, markdown_file)


# TODO: Create File

def createFile(content, markdown_file=markdown_file):
	with markdown_file.open('w') as f:
		for line in content:
			f.write(line)


# TODO: header

def header(markdown_file=markdown_file):
	""" Create File Header """

	header = """<h3 align="center">Derived from Open Source Society University
  <br>
  <br>
  <a href="https://github.com/open-source-society/data-science">
    <img alt="Open Source Society University - Data Science" src="https://img.shields.io/badge/OSSU-data--science-blue.svg"></h3>
  </a>
<p align="center">
  :bar_chart: Path to a free self-taught education in <strong>Data Science</strong>!
  <br><br>

</p>"""

	return header


# TODO: table of contents

def tableOfContents(markdown_file=markdown_file):
	""" Create File Table Of Contents """

	# get Table Of Contents raw data
	toc = resourcesdb.getMainCategories()

	# for Topic in toc
	for t in toc:
		print(f"- [{t.title()}](#{t.lower().replace(' ', '-')})")

tableOfContents()

# TODO: current year block

# TODO: courses on the road map block