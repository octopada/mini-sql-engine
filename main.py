from loader import Loader
from parser import Parser
from engine import Engine

database = Loader.get_database()

if __name__ == '__main__':

	while True:

		query = raw_input('> ')

		if query == 'Quit':

			break

		try:

			statement_data = Parser.process_query(query, database)
			Engine.execute(statement_data)

		except SyntaxError as error:

			print 'SyntaxError: ' + str(error)

		except NotImplementedError as error:

			print 'NotImplementedError: ' + str(error)

		except IndexError as error:

			print 'IndexError: ' + str(error)