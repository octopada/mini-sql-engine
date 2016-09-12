class Database:

	def __init__(self):

		self.tables = []
		self.tables_index = {}

	def __repr__(self):

		rep = 'database:\n'
		for table in self.tables:
			rep += table.__repr__()
			rep += '\n'

		return rep

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

	def get_table_by_name(self, table_name):		

		try:

			table_i = self.tables_index[table_name]
			return self.tables[table_i]

		except KeyError:

			raise KeyError('Table: "%s" does not exist' % (table_name))


class Table:

	def __init__(self, name):

		self.name = name
		self.columns = []
		self.columns_index = {}
		self.rows = []

	def __repr__(self):

		rep = 'Table: %s\n' % (self.name)
		for col in self.columns:
			rep += col.__repr__()
			rep += '\n'

		return rep

	def add_column(self, column_name):

		column = Column(self, column_name)

		self.columns_index[column_name] = len(self.columns)
		self.columns.append(column)

	def insert_values(self, row_data):

		row = Row(self)
		row.insert_values(row_data)
		self.rows.append(row)

	def get_name(self):

		return self.name

	def get_columns(self):

		return self.columns[:]

	def get_rows(self):

		return self.rows


class Row:

	def __init__(self, table):

		self.table = table
		self.cells = []

	def insert_values(self, row_data):

		columns = self.table.get_columns()

		for i, value in enumerate(row_data):

			cell = Cell(
				self, 
				columns[i], 
				row_data[i],
			)

			columns[i].append_cell(cell)
			self.cells.append(cell)

	def get_row_data(self):

		return [cell.get_value() for cell in self.cells]


class Column:

	def __init__(self, table, name):

		self.table = table
		self.name = name
		self.cells = []

	def __repr__(self):

		rep = 'Column: %s\n' % (self.name)
		for cell in self.cells:
			rep += cell.__repr__()
			rep += '\n'

		return rep

	def append_cell(self, cell):

		self.cells.append(cell)

	def get_name(self):

		return self.name


class Cell:

	def __init__(self, row, column, value):

		self.row = row
		self.column = column
		self.value = value

	def __repr__(self):

		return "cell value: %s" % self.value

	def get_value(self):

		return self.value