from loader import Loader
from parser import parse

database = Loader.get_database()

if __name__ == '__main__':

	query = ''
	while(query != 'Quit'):

		query = raw_input('> ')

		parse(query)
			
	# TESTING
	tables = database.get_tables()

	for i in range(len(tables)):
		print tables[i].name, "has columns:"
		for j in range(len(tables[i].columns)):
			print tables[i].columns[j].name, "has values:"
			for k in range(len(tables[i].columns[j].cells)):
				print tables[i].columns[j].cells[k]
