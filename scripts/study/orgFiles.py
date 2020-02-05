#!/usr/bin/env python3

import os
import shutil
import pathlib
import pprint

c = set()


extName = 'extensions'
dirNonExt = 'unknown_ext'
dirSubFolder = 'subDirectories'
termLength = 70
wantedDir = 'Downloads'

def getFiles(path, onlyFiles=True):
	""" List all files inside `path` and return a list of 'pathlib.PosixPath' objects """

	path = pathlib.Path(path)

	files = [ f for f in path.glob('*') if f.is_file() ]

	if onlyFiles:
		return files
	else:
		return (files, path)

def getDirectories(path, onlyDirs=True):
	""" List all directories inside `path` and return a list of 'pathlib.PosixPath' objects """

	path = pathlib.Path(path)
	directories = [ f for f in path.glob('*') if f.is_dir() ]
	if onlyDirs:
		return directories
	else:
		return (directories, path)

def makeDirExt(files):
	""" create a directory in `./extensions/` for each new file extension """

	if type(files) == tuple:
		files, path = files
	else:
		path = ''

	ext = set()
	[ ext.add(f.suffix) for f in files if f.suffix is not '' ]

	# There must to exist at least one file to create another directory
	if len(ext) > 0:
		parent = files[0].parent

		[ pathlib.Path.mkdir(pathlib.Path.joinpath(parent, extName, e.lstrip('.')), parents=True, exist_ok=True) for e in ext ]

		pathlib.Path.mkdir(pathlib.Path.joinpath(parent, extName, dirNonExt), parents=True, exist_ok=True)

	if path:
		# Also create directory `dirSubFolder`
		pathlib.Path.mkdir(pathlib.Path.joinpath(path, dirSubFolder), parents=True, exist_ok=True)


# TODO: write a function that move each file inside `path` to corresponding `./extensions/<ext>`

def mvFilesExt(path):
	""" Move all files to respective `extension` directorie """
	path = pathlib.Path(path)
	files = getFiles(path)
	for f in files:
		ext = f.suffix
		ext = ext.lstrip('.')
		if ext:
			# Get which `entension` the `file` have
			extDir = pathlib.Path.joinpath(path, extName, ext)
			# certify that subdirectory exists
			assert extDir.exists() and extDir.is_dir(), f"Directory {extDir} does not exist"
			# certify that does not already exists same file in same location
			oldFilePath = f.resolve()
			newFilePath = pathlib.Path.joinpath(extDir, f.name).resolve()
			assert not newFilePath.exists(), f"File {newFilePath} already exists"
			print(f"".center(termLength, '='))
			print(f'FILE: {f.name} '.ljust(termLength, '-'))
			print()
			print(f" MOVING ".center(termLength, '_'))
			print()
			print(f'· FROM: {oldFilePath}')
			print(f'· TO  : {newFilePath}')
			print()
			print(f"".center(termLength, '='))
			oldFilePath.rename(newFilePath)
		else:
			extDir = pathlib.Path.joinpath(path, extName, dirNonExt)
			assert extDir.exists() and extDir.is_dir(), f"Directory {extDir} does not exist"
			oldFilePath = f.resolve()
			newFilePath = pathlib.Path.joinpath(extDir, f.name).resolve()
			assert not newFilePath.exists(), f"File {newFilePath} already exists"
			print(f"".center(termLength, '='))
			print(f'FILE: {f.name} '.ljust(termLength, '-'))
			print()
			print(f" MOVING ".center(termLength, '_'))
			print()
			print(f'· FROM: {oldFilePath}')
			print(f'· TO  : {newFilePath}')
			print()
			print(f"".center(termLength, '='))
			oldFilePath.rename(newFilePath)

def mvDirectories(directories):
	""" Move all directories to subfolder `subDirectories` """

	for d in directories:
		if d.name == dirSubFolder:
			continue
		elif d.name == extName:
			continue
		oldDirPath = d.resolve()
		newDirPath = pathlib.Path.joinpath(d.parent, dirSubFolder, d.name)
		assert not newDirPath.exists(), f"Directory {newDirPath} already exists"
		print(f"".center(termLength, '='))
		print(f'Directory: {d.name} '.ljust(termLength, '-'))
		print()
		print(f" MOVING ".center(termLength, '_'))
		print()
		print(f'· FROM: {oldDirPath}')
		print(f'· TO  : {newDirPath}')
		print()
		print(f"".center(termLength, '='))
		print()
		oldDirPath.rename(newDirPath)


# TODO: write a function that loop for every subfolder of `path`, find empty directories and delete them

def findUsersDirs(wantedDir, shallowSearch=True):
	""" find `wantedDir` for each User """

	home = pathlib.Path('/home').resolve()
	users = [ u for u in home.glob('*')]

	dirs = []
	for u in users:
		if shallowSearch:
			directory = list(u.glob(wantedDir))
		else:
			directory = list(u.rglob(wantedDir))

		if directory:
			dirs.append(directory)

	dirs = [ i for i in dirs if i ]

	return dirs

# Main Funtion

def main(path):
	""" This function handle all necessary things to organize directory """

	makeDirExt(getFiles(path, onlyFiles=False))
	mvFilesExt(path)
	mvDirectories(getDirectories(path))

if __name__ == '__main__':

	dirs = findUsersDirs(wantedDir)
	[ [ main(path) for path in user ] for user in dirs ]
