import sqlparse
from loader import Loader

if __name__ == '__main__':

	database = Loader.get_database()

	query = ''
	while(query != 'Quit'):
		
		query = raw_input('> ')
		parsed = sqlparse.parse(query)
		print parsed

	# TESTING
	tables = database.get_tables()

	for i in range(len(tables)):
		print tables[i].name, "has columns:"
		for j in range(len(tables[i].columns)):
			print tables[i].columns[j].name, "has values:"
			for k in range(len(tables[i].columns[j].values)):
				print tables[i].columns[j].values[k]