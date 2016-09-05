d = {'a':1, 'b':2, 'op': '*'}

def calc(**operands):
	print operands['a']

	if operands.pop('b', None)