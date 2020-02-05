#!/usr/bin/env python3

import os
import shutil
import pathlib
import pprint

c = set()

def getFiles(path):
	""" List all files inside `path` and return a list of 'pathlib.PosixPath' objects """

	files = [ f for f in pathlib.Path(path).glob('*') if f.is_file() ]
	return (files)

def makeDirExt(files):
	""" create a directory in `./extensions/` for each new file extension """

	ext = set()
	[ ext.add(f.suffix) for f in files if f.suffix is not '' ]

	parent = files[0].parent

	[ pathlib.Path.mkdir(pathlib.Path.joinpath(parent, 'extensions', e.lstrip('.')), parents=True, exist_ok=True) for e in ext ]


# TODO: write a function that move each file inside `path` to corresponding `./extensions/<ext>`

def mvFilesExt(path):
	files = getFiles(path)
	print(files)



# TODO: write a function that loop for every subfolder of `path`, find empty directories and delete them
# makeDirExt(getFiles('/home/matheus/Downloads'))
mvFilesExt('/home/matheus/Downloads')
