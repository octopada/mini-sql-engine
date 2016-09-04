class Table:

	def __init__(self, name):

		self.name = name
		self.columns = []

	def add_column(self, column_name):

		self.columns.append(Column(column_name))

	def insert_values(self, row_data):

		for i, col in enumerate(self.columns):

			col.insert_value(row_data[i])

	def get_name(self):

		return self.name


class Column:

	def __init__(self, name):

		self.name = name
		self.values = []

	def insert_value(self, value):

		self.values.append(value)


class Database:

	def __init__(self):

		self.tables = []
		self.tables_index = {}

	def create_table(self, table_name, column_names):

		table = Table(table_name)
		
		for col in column_names:

			table.add_column(col)

		self.tables_index[table_name] = len(self.tables)
		self.tables.append(table)

	def insert_values(self, table_name, row_data):

		table_ind = self.tables_index[table_name]
		table = self.tables[table_ind]

		table.insert_values(row_data)

	def get_tables(self):

		tables = self.tables[:]
		return tables