from loader import Loader
from parser import Parser

database = Loader.get_database()

if __name__ == '__main__':

	while True:

		query = raw_input('> ')

		if query == 'Quit':

			break

		statement_data = Parser.process_query(query, database)
		print statement_data

	print database