#!/usr/bin/env python3

import re
import os
import sys
import shutil
import pathlib

directory = pathlib.Path("/home/matheus/mcs")

r = r'^[\s\w\/\(\)\[\]~\_\.\-\@\+\#\=\{\}\%\,\'\"\—\º\ªíáõãé🤘🏽🙌🏻💉🤩]*$'

nonUTF8 = re.compile(r, re.IGNORECASE)
clean = re.compile(r.strip('^$'), re.IGNORECASE)

non = set()

for file in directory.rglob('*'):
	f = str(file)
	mo = nonUTF8.search(f)
	if not mo:
		print('='*30)
		print(file)
		print(f)
		print(mo)
		print('='*30)
		# print(g)
		g = list(clean.sub('', f).strip())
		[non.add(x) for x in g]

print(non)
print(list(non))

