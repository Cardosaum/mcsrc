#!/usr/bin/env python3

######### Configuration #########

# Paths
logPath = 'logs'
scriptPath = 'script'

# Files
logFile = 'logFile.txt'

#################################


import pathlib


# Setup paths
logPath = pathlib.Path(logPath)
scriptPath = pathlib.Path(scriptPath)

# Setup files
logFile = pathlib.Path.joinpath(logPath, logFile)


def mkDirs():
	""" Create default paths """

	cdp = []
	cdp.append(logPath)
	cdp.append(scriptPath)

	[ p.mkdir(exist_ok=True) for p in cdp ]


if __name__ == '__main__':

	mkDirs()
