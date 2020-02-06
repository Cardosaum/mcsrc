#!/usr/bin/env python3

import subprocess
import pprint
import re
import csv
import collections
import ulogme_setup


logPath = ulogme_setup.logPath
logFile = 

###########################


# collect data

	# window properties

def getRootProps(returnNested=False):
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
	# rerNAW = re.compile(r'^(_NET_ACTIVE_WINDOW).*?[=#:]{1}\s*window\s+id\s+#\s+(.*)$')
	# rerNDN = re.compile(r'^(_NET_DESKTOP_NAMES).*?[=#:]\s+(.*)$')
	# rerNND = re.compile(r'^(_NET_NUMBER_OF_DESKTOPS).*?[=#:]\s+(.*)$')
	# rerNCL = re.compile(r'^(_NET_CLIENT_LIST).*[=#:]\s+window\s+id\s+#\s+(.*)$')
	# rerNCD = re.compile(r'^(_NET_CURRENT_DESKTOP).*?[=#:]\s+(.*)$')
	# rerNWN = re.compile(r'^(_NET_WM_NAME).*?[=#:]\s+(.*)$')
	rerNAW = re.compile(r'^(_NET_ACTIVE_WINDOW)(:\s*[=:].*#\s*|\(WINDOW\)\s*[=:].*#\s*) (.*)$')
	rerNDN = re.compile(r'^(_NET_DESKTOP_NAMES)(:|\(UTF8_STRING\) =) (.*)$')
	rerNND = re.compile(r'^(_NET_NUMBER_OF_DESKTOPS)(:|\(CARDINAL\) =) (.*)$')
	rerNCL = re.compile(r'^(_NET_CLIENT_LIST)(:\s*[=:].*#\s*|\(WINDOW\)\s*[=:].*#\s*) (.*)$')
	rerNCD = re.compile(r'^(_NET_CURRENT_DESKTOP)(:|\(CARDINAL\) =) (.*)$')
	rerNWN = re.compile(r'^(_NET_WM_NAME)(:|\(UTF8_STRING\) =) (.*)$')

	rootRegexs.append(rerNAW)
	rootRegexs.append(rerNDN)
	rootRegexs.append(rerNND)
	rootRegexs.append(rerNCL)
	rootRegexs.append(rerNCD)
	rootRegexs.append(rerNWN)


	# Get raw properties
	root = subprocess.getoutput(f'xprop -root {rootPropsStr}').splitlines()

	# matched objects root
	mor = assertRegexMatch(rootRegexs, root)

	# Convert list of matched objects in list of tuple of strings `(key, value)`
	mor = [ (mor[i].groups()[0], mor[i].groups()[-1]) for i in range(len(mor)) ]
	mor = [ (str('root-'+mor[i][0]), str(mor[i][1])) for i in range(len(mor)) ]

	if returnNested:
		return mor

	# transform nested list in a dictionary
	else:
		d = collections.defaultdict(list)
		[ d[k].append(v) for k, v in mor]

		return d


def getWindowProps(winID, returnNested=False):
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
	# rewNWS = re.compile(r'^(_NET_WM_STATE).*?[=#:]\s+(.*)$')
	# rewNWD = re.compile(r'^(_NET_WM_DESKTOP).*?[=#:]\s+(.*)$')
	# rewWWR = re.compile(r'^(WM_WINDOW_ROLE).*[=#:] (.*)$')
	# rewNWWT = re.compile(r'^(_NET_WM_WINDOW_TYPE).*[=#:] (.*)$')
	# rewWN = re.compile(r'^(WM_NAME).*[=#:] (.*)$')
	# rewNWN = re.compile(r'^(_NET_WM_NAME).*[=#:] (.*)$')
	# rewWCM = re.compile(r'^(WM_CLIENT_MACHINE).*[=#:] (.*)$')
	# rewWC = re.compile(r'^(WM_CLASS).*[=#:] (.*)$')
	rewNWS = re.compile(r'^(_NET_WM_STATE)(:|\(ATOM\) =) (.*)$')
	rewNWD = re.compile(r'^(_NET_WM_DESKTOP)(:|\(CARDINAL\) =) (.*)$')
	rewWWR = re.compile(r'^(WM_WINDOW_ROLE)(:|\(STRING\) =) (.*)$')
	rewNWWT = re.compile(r'^(_NET_WM_WINDOW_TYPE)(:|\(ATOM\) =) (.*)$')
	rewWN = re.compile(r'^(WM_NAME)(:|\(STRING\) =) (.*)$')
	rewNWN = re.compile(r'^(_NET_WM_NAME)(:|\(UTF8_STRING\) =) (.*)$')
	rewWCM = re.compile(r'^(WM_CLIENT_MACHINE)(:|\(STRING\) =) (.*)$')
	rewWC = re.compile(r'^(WM_CLASS)(:|\(STRING\) =) (.*)$')


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
	mow = assertRegexMatch(winRegexs, win)

	# Convert list of matched objects in list of tuple of strings `(key, value)`
	mow = [ (mow[i].groups()[0], mow[i].groups()[-1]) for i in range(len(mow)) ]
	mow = [ (str('win-'+mow[i][0]), str(mow[i][1])) for i in range(len(mow)) ]

	if returnNested:
		return mow

	# transform nested list in a dictionary
	else:
		d = collections.defaultdict(list)
		[ d[k].append(v) for k, v in mow]
		return d




	# work in each prop, and handle specifities, especificaly with `WM_CLASS`


def assertRegexMatch(regexList, listSearch, ret="mo"):
	""" Get raw data in form of list and return all matched items. 
		The items that weren't matched are writed to a log file
	"""

	# list of matched objects
	mo = []

	# list of lines that were'n matched by any regex (Not Match Objects)
	nmo = []


	# loop all items and get regex match objects of them
	n = len(regexList)

	for i in listSearch:
		c = listSearch.index(i)
		for r in regexList:
			m = r.search(i)
			if m:
				mo.append(m)
				break
		if not m:
			nmo.append(i)

	if nmo:
		print(nmo)
		with open(lf, mode='a') as l:
			[ l.write(i + '\n') for i in nmo ]


	if ret == "mo":
		return mo
	elif ret == "nmo":
		return nmo
	else:
		return (mo, nmo)



def sortNested(nestedList, nth):
	""" sort nested list in this way:

	Input : [['rishav', 10], ['akash', 5], ['ram', 20], ['gaurav', 15]]
	Output : [['akash', 5], ['rishav', 10], ['gaurav', 15], ['ram', 20]]

	Input : [['452', 10], ['256', 5], ['100', 20], ['135', 15]]
	Output : [['256', 5], ['452', 10], ['135', 15], ['100', 20]]

	copied from: https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
	"""

	return(sorted(nestedList, key=lambda x: x[nth]))

	# TODO: property `_NET_CLIENT_LIST` show id for all open windows. Maybe it's useful?


def loopOpenWindows():
	""" loop for all open windows and return their properties 
		In this form:

		dict = 

		{
			'IDx': defaultdict(<dict_IDx>),
			'IDy': defaultdict(<dict_IDy>),
			.
			.
			.
			---snip---
			'IDz': defaultdict(<dict_IDz>),
		}

		"""


	# get open windows
	ow = getRootProps()
	ow = [ i.strip() for i in ow['root-_NET_CLIENT_LIST'][0].split(',') ]


	# get property for each window
	owp = collections.defaultdict(dict)
	for w in ow:
		owp[w] = getWindowProps(w)

	# clean property strings
	for wId, wVal in owp.items():
		# print(wId, wVal)
		if wId == '0x1600007':
			print(wVal)
			for k, v in wVal.items():
				print(k, v)


	return owp


# pprint.pprint(getWindowProps('0x5600001'))
# pprint.pprint(getWindowProps('0x3400003'))
# pprint.pprint(getWindowProps('0x1600007'))
# pprint.pprint(getWindowProps('0x2800007'))
"""
###################
#
# Corrigir regex 
#
###################

#####
##### essas são propriedades da janela aberta:
#####

WM_NAME(STRING) = "~ : htop"
_NET_WM_NAME(UTF8_STRING) = "~ : htop — Konsole"
_MOTIF_WM_HINTS(_MOTIF_WM_HINTS) = 0x3, 0x3e, 0x7e, 0x0, 0x0
_NET_WM_WINDOW_TYPE(ATOM) = _NET_WM_WINDOW_TYPE_NORMAL
_XEMBED_INFO(_XEMBED_INFO) = 0x0, 0x1
WM_CLIENT_LEADER(WINDOW): window id # 0x1600009
WM_HINTS(WM_HINTS):
                Client accepts input or input focus: True
                Initial state is Normal State.
                window id # of group leader: 0x1600009
WM_CLIENT_MACHINE(STRING) = "mcsarch"
_NET_WM_PID(CARDINAL) = 5282
_NET_WM_SYNC_REQUEST_COUNTER(CARDINAL) = 23068680
WM_CLASS(STRING) = "konsole", "konsole"


#####
##### essas são as propriedades retornadas pela função
#####

win-_NET_WM_STATE ['_NET_WM_STATE_MAXIMIZED_HORZ, _NET_WM_STATE_MAXIMIZED_VERT']
win-_NET_WM_DESKTOP ['1']
win-WM_WINDOW_ROLE ['"MainWindow#1"']
win-_NET_WM_WINDOW_TYPE ['_NET_WM_WINDOW_TYPE_NORMAL']
win-WM_NAME ['htop"']
win-_NET_WM_NAME ['htop — Konsole"']
win-WM_CLIENT_MACHINE ['"mcsarch"']
win-WM_CLASS ['"konsole", "konsole"']


## Variável `win-_NET_WM_NAME` está sendo retornada errada

"""
getRootProps()
# loopOpenWindows()
# getWindowProps('0x0')
# print(''.center(70, '='))
getWindowProps('0x4600001')
# print(''.center(70, '='))
# getWindowProps('0x5a00003')
# getWindowProps('0x4000007')
# getWindowProps('0x4c00007')
# print(getRootProps())
# getRootProps()
# a = getWindowProps('0x2e00003')
# b = getRootProps()
# c = sortNested(a + b, 0)
# [ print(i, end=',') for i in c ]
# createLogFile('test_log.csv')


# w = loopOpenWindows()

# for k, v in w.items():
# 	print(k)
# 	pprint.pprint(v)

# print(w['0x2a00003']['win-WM_NAME'])

	# TODO: keyboard input
	# TODO: mouse input (?)

# TODO: tidy data
	# TODO: chose beteween csv or json (or something else)
	# TODO: write a decent file handler
def createLogFile(file):
	header = 'root-_NET_ACTIVE_WINDOW,root-_NET_CLIENT_LIST,root-_NET_CURRENT_DESKTOP,root-_NET_DESKTOP_NAMES,root-_NET_NUMBER_OF_DESKTOPS,root-_NET_WM_NAME,win-WM_CLASS,win-WM_CLIENT_MACHINE,win-WM_NAME,win-WM_WINDOW_ROLE,win-_NET_WM_DESKTOP,win-_NET_WM_NAME,win-_NET_WM_STATE,win-_NET_WM_WINDOW_TYPE'.split(',')
	with open(file, 'w') as f:
		w = csv.writer(f)
		w.writerow(header)
	# TODO: write data to file
