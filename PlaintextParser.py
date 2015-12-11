from Course import *

FILE_NAME = "ics31.txt"
OUT_FILE_NAME = "output.txt"

def isInt(input: str) -> int:
	""" Checks if input str contains an integer. """
	try:
		int(input)
		return True
	except Exception:
		return False
assert isInt('534')
assert isInt('-534')
assert isInt('0')
assert isInt('-0')
assert not isInt('a0')
assert not isInt('0a')
assert not isInt('asdf')

lines = []
datas = []
classes = []

with open(FILE_NAME, 'r') as f:
	for line in f:
		if line.startswith('    ') and isInt(line[4:10]):
			lines.append(line)
			raw_tuple = (line[4:10], line[10:14], line[14:18], line[18:22], line[22:35], line[35:40], 
						line[40:53], line[53:62], line[62:87], line[87:91], line[91:102],
						line[102:106], line[106:112], line[112:114], line[114:119], line[119:])
			stripped_tuple = tuple([el.strip() for el in raw_tuple])
			datas.append(stripped_tuple)
			classes.append(Class(stripped_tuple))

with open(OUT_FILE_NAME, 'w') as f:
	for line in lines:
		f.write(line)
	f.write('\n\n')
	for data in datas:
		f.write("\t\t".join(data) + '\n')
	f.write('\n\n')
	for data in datas:
		f.write(str(data) + '\n')
	for curr_class in classes:
		f.write(str(curr_class) + '\n')