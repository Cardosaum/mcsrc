#!/usr/bin/env python3

import subprocess
import re

# TODO: collect data

	# TODO: window properties

def getRootProps():
	""" Get this window properties:

	_NET_ACTIVE_WINDOW
	_NET_DESKTOP_NAMES
	_NET_NUMBER_OF_DESKTOPS
	_NET_CLIENT_LIST
	_NET_CURRENT_DESKTOP
	_NET_WM_NAME
	"""


	# root properties wanted
	rootProps = []
	rootProps.append('_NET_ACTIVE_WINDOW')
	rootProps.append('_NET_DESKTOP_NAMES')
	rootProps.append('_NET_NUMBER_OF_DESKTOPS')
	rootProps.append('_NET_CLIENT_LIST')
	rootProps.append('_NET_CURRENT_DESKTOP')
	rootProps.append('_NET_WM_NAME')
	rootPropsStr = ' '.join(rootProps)


	# regex for root properties
	rootRegexs = []
	rerNAW = re.compile(r'^(_NET_ACTIVE_WINDOW).*[=#:] (.*)$')
	rerNDN = re.compile(r'^(_NET_DESKTOP_NAMES).*[=#:] (.*)$')
	rerNND = re.compile(r'^(_NET_NUMBER_OF_DESKTOPS).*[=#:] (.*)$')
	rerNCL = re.compile(r'^(_NET_CLIENT_LIST).*[=#:] (.*)$')
	rerNCD = re.compile(r'^(_NET_CURRENT_DESKTOP).*[=#:] (.*)$')
	rerNWN = re.compile(r'^(_NET_WM_NAME).*[=#:] (.*)$')

	rootRegexs.append(rerNAW)
	rootRegexs.append(rerNDN)
	rootRegexs.append(rerNND)
	rootRegexs.append(rerNCL)
	rootRegexs.append(rerNCD)
	rootRegexs.append(rerNWN)


	# Get raw properties
	root = subprocess.getoutput(f'xprop -root {rootPropsStr}').splitlines()


	# matched objects root
	mor = []

	# Loop all properties and get regex match
	for prop in root:
		for rRegex in rootRegexs:
			m = rRegex.search(prop)
			if m:
				mor.append(m)
				break

	# Convert list of matched objects in list of tuple of strings `(key, value)`
	mor = [tuple(mor[i].groups()) for i in range(len(mor))]

	return mor






def getWindowProps(winID):
	""" Get this window properties:
	
	_NET_WM_STATE
	_NET_WM_DESKTOP
	WM_WINDOW_ROLE
	_NET_WM_WINDOW_TYPE
	WM_NAME
	_NET_WM_NAME
	WM_CLIENT_MACHINE
	WM_CLASS
	"""

	# window properties wanted
	winProps = []
	winProps.append('_NET_WM_STATE')
	winProps.append('_NET_WM_DESKTOP')
	winProps.append('WM_WINDOW_ROLE')
	winProps.append('_NET_WM_WINDOW_TYPE')
	winProps.append('WM_NAME')
	winProps.append('_NET_WM_NAME')
	winProps.append('WM_CLIENT_MACHINE')
	winProps.append('WM_CLASS')
	winPropsStr = ' '.join(winProps)

	# regex for window properties
	winRegexs = []
	rewNWS = re.compile(r'^(_NET_WM_STATE).*[=#:] (.*)$')
	rewNWD = re.compile(r'^(_NET_WM_DESKTOP).*[=#:] (.*)$')
	rewWWR = re.compile(r'^(WM_WINDOW_ROLE).*[=#:] (.*)$')
	rewNWWT = re.compile(r'^(_NET_WM_WINDOW_TYPE).*[=#:] (.*)$')
	rewWN = re.compile(r'^(WM_NAME).*[=#:] (.*)$')
	rewNWN = re.compile(r'^(_NET_WM_NAME).*[=#:] (.*)$')
	rewWCM = re.compile(r'^(WM_CLIENT_MACHINE).*[=#:] (.*)$')
	rewWC = re.compile(r'^(WM_CLASS).*[=#:] (.*)$')

	winRegexs.append(rewNWS)
	winRegexs.append(rewNWD)
	winRegexs.append(rewWWR)
	winRegexs.append(rewNWWT)
	winRegexs.append(rewWN)
	winRegexs.append(rewNWN)
	winRegexs.append(rewWCM)
	winRegexs.append(rewWC)

	# Get raw properties
	win = subprocess.getoutput(f'xprop -id {winID} {winPropsStr}').splitlines()

	# matched objects window
	mow = []

	# Loop all properties and get regex match
	for prop in win:
		for rRegex in winRegexs:
			m = rRegex.search(prop)
			if m:
				mow.append(m)
				break

	# Convert list of matched objects in list of tuple of strings `(key, value)`
	mow = [tuple(mow[i].groups()) for i in range(len(mow))]
	mow = [ (str('win-'+mow[i][0]), str(mow[i][1]))for i in range(len(mow))]

	return mow



# work in each prop, and handle specifities, especificaly with `WM_CLASS`

# getWindowProps('0x0')
getWindowProps('0x2e00003')
# print(''.center(70, '='))
# getWindowProps('0x2400007')
# getWindowProps('0x4200007')
# getWindowProps('0x4600001')
# print(''.center(70, '='))
# getWindowProps('0x5a00003')
# getWindowProps('0x4000007')
# getWindowProps('0x4c00007')
getRootProps()



























	# TODO: property `_NET_CLIENT_LIST` show id for all open windows. Maybe it's useful?



	# TODO: keyboard input
	# TODO: mouse input (?)

# TODO: tidy data
	# TODO: chose beteween csv or json (or something else)
	# TODO: write data to file
