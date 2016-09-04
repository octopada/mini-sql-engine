import sqlparse
from sqlparse import tokens
from loader import Loader

if __name__ == '__main__':

	database = Loader.get_database()

	query = ''
	while(query != 'Quit'):

		query = raw_input('> ')

		parsed_query = sqlparse.parse(query)
		query_tokens = parsed_query[0].tokens

		if query_tokens[0].match(tokens.DML, 'SELECT'):

			if query_tokens[2].match(tokens.Wildcard, '*', regex = False):

				print 'select all'

			elif query_tokens[2].match(None, '.*', regex = True):

				cols = str(query_tokens[2].value)
				print 'select', cols

			else:

				print 'error'

			if not query_tokens[4].match(
					tokens.Keyword, 'FROM', regex = False):

				print 'error'

			if query_tokens[6].match(None, '.*', regex = True):

				tables = str(query_tokens[6].value)
				print 'from', tables

			else:

				print 'error'

		else:

			print 'error'

				
	# TESTING
	tables = database.get_tables()

	for i in range(len(tables)):
		print tables[i].name, "has columns:"
		for j in range(len(tables[i].columns)):
			print tables[i].columns[j].name, "has values:"
			for k in range(len(tables[i].columns[j].cells)):
				print tables[i].columns[j].cells[k]
