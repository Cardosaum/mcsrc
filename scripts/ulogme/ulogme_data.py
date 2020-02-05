#!/usr/bin/env python3

import subprocess


def getRootProps():
	""" Get this window properties:

	_NET_ACTIVE_WINDOW
	_NET_DESKTOP_NAMES
	_NET_NUMBER_OF_DESKTOPS
	_NET_CLIENT_LIST
	_NET_CURRENT_DESKTOP
	_NET_WM_NAME
	"""

	rootProps = []
	rootProps.append('_NET_ACTIVE_WINDOW')
	rootProps.append('_NET_DESKTOP_NAMES')
	rootProps.append('_NET_NUMBER_OF_DESKTOPS')
	rootProps.append('_NET_CLIENT_LIST')
	rootProps.append('_NET_CURRENT_DESKTOP')
	rootProps.append('_NET_WM_NAME')
	rootPropsStr = ' '.join(rootProps)
	root = subprocess.getoutput(f'xprop -root {rootPropsStr}')
	# print(root)



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
	win = subprocess.getoutput(f'xprop -id {winID} {winPropsStr}')

	print(win)


# TODO: property `_NET_CLIENT_LIST` show id for all open windows. Maybe it's useful?

getWindowProps('0x4600001')