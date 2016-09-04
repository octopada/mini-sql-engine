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

class Table:

	def __init__(self, name):

		self.name = name
		self.columns = []
		self.rows = []

	def add_column(self, column_name):

		column = Column(self, column_name)
		self.columns.append(column)

	def insert_values(self, row_data):

		row = Row(self)
		row.insert_values(row_data)

	def get_name(self):

		return self.name

	def get_columns(self):

		return self.columns[:]

class Row:

	def __init__(self, table):

		self.table = table
		self.cells = []

	def insert_values(self, row_data):

		columns = self.table.get_columns()

		for i, value in enumerate(row_data):

			cell = Cell(self, columns[i], row_data[i])

			columns[i].append_cell(cell)
			self.cells.append(cell)

class Column:

	def __init__(self, table, name):

		self.table = table
		self.name = name
		self.cells = []

	def append_cell(self, cell):

		self.cells.append(cell)

class Cell:

	def __init__(self, row, column, value):

		self.row = row
		self.column = column
		self.value = value

	def __repr__(self):

		return "cell value: %s" % self.value