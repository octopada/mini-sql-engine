import sys
from loader import Loader

class Engine:

	database = Loader.get_database()

	@classmethod
	def execute(cls, statement_data):

		if statement_data['command'] == 'SELECT':

			table_names = statement_data['table_ids']

			cls.joined_table = cls.process_tables(table_names)

			if statement_data['has_where']:

				cls.filtered_table = cls.filter_by_where(statement_data['where_clause'])

			else:

				cls.filtered_table = cls.joined_table

			if statement_data['has_function']:

				Engine.aggregate_function(statement_data, cls.filtered_table)

			else:

				column_names = statement_data['column_ids']
				selected_columns = cls.process_columns(column_names)

				cls.project(selected_columns)

		else:

			raise NotImplementedError('Command not implemented')


	@classmethod
	def project(cls, columns):

		print '%s' % ', '.join(map(str, columns))

		rows = cls.filtered_table.get_rows()
		for row in rows:

			projected_row_data = []
			cells = row.get_cells()
			for cell in cells:

				cell_column = cell.get_column()
				if cell_column.get_name() in columns:

					projected_row_data.append(cell.get_value())

			print '%s' % ', '.join(map(str, projected_row_data))


	@classmethod
	def process_columns(cls, column_names):

		selected_columns = []

		if column_names[0] == '*': # handle Wildcard

			columns = cls.filtered_table.get_columns()

			for column in columns:

				selected_columns.append(str(column.get_name()))

		else:

			for column_name in column_names:

				if not '.' in column_name:

					columns = cls.filtered_table.get_columns()

					for column in columns:

						proper_column_name = column.get_name()
						half_column_name = proper_column_name.split('.')

						if column_name == half_column_name[1]:

							column_name = proper_column_name

				selected_columns.append(str(column_name))

		return selected_columns


	@classmethod
	def process_tables(cls, table_names):

		tables = []
		column_names = []
		for table_name in table_names:

			table = cls.database.get_table_by_name(table_name)

			tables.append(table)

			columns = table.get_columns()

			for column in columns:

				column_name = column.get_name()
				column_names.append(table_name + '.' + column_name)

		cls.database.create_table('joined_table', column_names)
		joined_table = cls.database.get_table_by_name('joined_table')

		all_rows = []
		Engine.join(0, tables, [], all_rows) # generate rows

		for row in all_rows:

			joined_table.insert_values(row) # insert rows

		return joined_table


	@staticmethod
	def join(table_ind, tables, row_data, all_rows):

		if table_ind == len(tables):

			all_rows.append(row_data)

		else:

			table = tables[table_ind]

			for row in table.get_rows():

				new_row = row_data + row.get_row_data()
				Engine.join(table_ind + 1, tables, new_row, all_rows)


	@classmethod
	def filter_by_where(cls, where_clause):

		if len(where_clause) < 3 or (
				len(where_clause) > 3 and len(where_clause) < 7) or (
				len(where_clause) > 7):

			raise SyntaxError('Invalid WHERE clause')

		column_names = [column.get_name() for column in cls.joined_table.get_columns()]
		cls.database.create_table('filtered_table', column_names)
		filtered_table = cls.database.get_table_by_name('filtered_table')

		and_clause = False
		or_clause = False
		try:

			if where_clause[3].upper() == 'AND':

				and_clause = True

			elif where_clause[3].upper() == 'OR':

				or_clause = True

			else:

				raise SyntaxError('Invalid WHERE clause')

		except IndexError:

			pass

		rows = cls.joined_table.get_rows()
		for row_number, row in enumerate(rows):

			bool_1 = cls.compare(where_clause[0], where_clause[2], row_number)

			bool_2 = True

			if and_clause or or_clause:

				bool_2 = cls.compare(where_clause[4], where_clause[6], row_number)

			if and_clause:

				if bool_1 and bool_2:

					filtered_table.insert_values(row.get_row_data())

			elif or_clause:

				if bool_1 or bool_2:

					filtered_table.insert_values(row.get_row_data())

			else:

				if bool_1:

					filtered_table.insert_values(row.get_row_data())

		return filtered_table


	@classmethod
	def compare(cls, lhs, rhs, row_number):

		lhs_value = cls.get_value_from_argument(lhs, row_number)
		rhs_value = cls.get_value_from_argument(rhs, row_number)

		return lhs_value == rhs_value


	@classmethod
	def get_value_from_argument(cls, argument, row_number):

		column_argument = None

		if '.' in argument:

			column_argument = cls.joined_table.get_column_by_name(argument)

		else:

			columns = cls.joined_table.get_columns()

			for column in columns:

				proper_column_name = column.get_name()
				column_name = proper_column_name.split('.')

				if argument == column_name[1]:

					column_argument = column
					break

		if column_argument is not None:

			cell = column_argument.get_cell_by_index(row_number)
			return cell.get_value()
		
		return argument


	@staticmethod
	def aggregate_function(statement_data, table):

		function_column_name = statement_data['function_column']
		if not '.' in function_column_name:

			columns = table.get_columns()

			for column in columns:

				proper_column_name = column.get_name()
				column_name = proper_column_name.split('.')

				if function_column_name == column_name[1]:

					function_column_name = proper_column_name

		function_column = table.get_column_by_name(function_column_name)
		cells = function_column.get_cells()

		if statement_data['function'] == 'sum':

			ret = 0
			for cell in cells:

				ret += int(cell.get_value())

			print 'sum(' + function_column_name + ')'

		elif statement_data['function'] == 'avg':

			ret = 0
			for cell in cells:

				ret += int(cell.get_value())

			ret = float(ret)/len(cells)

			print 'avg(' + function_column_name + ')'

		elif statement_data['function'] == 'min':

			ret = sys.maxint
			for cell in cells:

				value = int(cell.get_value())
				if ret > value:
					
					ret = value

			print 'min(' + function_column_name + ')'

		elif statement_data['function'] == 'max':

			ret = -sys.maxint - 1
			for cell in cells:

				value = int(cell.get_value())
				if ret < value:

					ret = value

			print 'max(' + function_column_name + ')'

		else:

			raise NotImplementedError('Aggregate function not implemented or invalid')

		print ret