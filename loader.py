import re
from database import Database

class Loader:

	METADATA_FILE_NAME = 'metadata.txt'
	already_initialized = False
	database = Database()

	@classmethod
	def get_database(cls):

		if not cls.already_initialized:

			cls.initialize_database()
			cls.populate_database()
			cls.already_initialized = True

		return cls.database

	@classmethod
	def initialize_database(cls):

		line_is_table = False
		line_is_column = False

		metadata_file = open(cls.METADATA_FILE_NAME)
		metadata_lines = metadata_file.readlines()

		for line in metadata_lines:

			if line_is_column:

				if re.match('<end_table>.*', line):

					cls.database.create_table(cls.table_name, cls.column_names)
					line_is_column = False

				else:

					column_name = line.strip()
					cls.column_names.append(column_name)

			if line_is_table:

				cls.table_name = line.strip()
				line_is_table = False

				line_is_column = True
				cls.column_names = []

			if re.match('<begin_table>.*', line): # check for begin_table

				line_is_table = True

	@classmethod
	def populate_database(cls):

		tables = cls.database.get_tables()

		for table_it in range(len(tables)):

			table_name = tables[table_it].get_name()
			tabledata = open(table_name + '.csv')
			tabledata_rows = tabledata.readlines()

			for row in tabledata_rows:

				data = row.strip()
				data = data.split(',')
				cls.database.insert_values(table_name, data)