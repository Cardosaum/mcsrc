import os
import shutil
import sys
import glob
import pathlib

files = pathlib.Path("/home/matheus/mcs")
# files = pathlib.Path("/home/matheus/001_Matheus_(Backup)_12.08.2018")

change = {'Σ': 'õ', '╞': 'ã', '╟': 'Ã'}
c = list(change.keys())

for f in files.rglob('*'):
	i = [ x for x in list(str(f)) if x in c]
	if i:
		if 'Telegram Desktop' in str(f):
			print('skipping'.upper().center(100, '+'))
			print(f"{'file:'.upper()}\t{str(f)}")
			print('skipping'.upper().center(100, '+'))
			print()
			continue
		table = str.maketrans(change)
		old_file_name = str(f)
		new_file_name = str(f).translate(table)
		print('renaming file'.upper().center(50, '='))
		print(f"OLD:\t{old_file_name}")
		print(f"NEW:\t{new_file_name}")
		# shutil.move(old_file_name, new_file_name)
		print('renaming file'.upper().center(50, '='))
		print()
		# f_old = (str(f))
		# f_new = (str(f).replace(old, new))
		# print(f_old, f_new)
		# shutil.move(f_old, f_new)
