import sqlparse
from sqlparse import tokens
from database import Database, Table
from loader import Loader

database = Loader.get_database()

def join(table_ind, tables, row_data, all_rows):

	if table_ind == len(tables):

		all_rows.append(row_data)

	else:

		table = tables[table_ind]

		for row in table.get_rows():

			new_row = row_data + row.get_row_data()
			join(table_ind + 1, tables, new_row, all_rows)


def process_tables(tables):

	if not tables.match(None, '.*', regex = True):

		raise ValueError('Invalid Tables')

	table_names = str(tables.value)
	tables_list = table_names.split(',')

	stripped_tables_list = []
	for table_name in tables_list:

		stripped_tables_list.append(table_name.strip())

	joined_table = Table('joined_table')

	tables = [database.get_table_by_name(table_name) for table_name in stripped_tables_list]

	for table in tables: # join columns

		for col in table.get_columns():

			joined_table.add_column(table.get_name() + '#' + col.get_name())

	all_rows = []
	join(0, tables, [], all_rows) # generate rows

	for row in all_rows:

		joined_table.insert_values(row) # insert rows

	return joined_table
	

def process_columns(columns, joined_table):

	selected_columns = []
	if columns.match(tokens.Wildcard, '*'):

		for col in joined_table.get_columns():

			selected_columns.append(col.get_name())

	return selected_columns


def parse(query):

	parsed_query = sqlparse.parse(query)
	query_tokens = parsed_query[0].tokens

	select_statement, columns, from_statement, tables = (
			[query_tokens[i] for i in range(0, 7, 2)])

	if not ((select_statement.match(tokens.DML, 'SELECT')) and (
			from_statement.match(tokens.Keyword, 'FROM'))):

		raise SyntaxError('Invalid Query')

	joined_table = process_tables(tables)

	selected_columns = process_columns(columns, joined_table)

	print joined_table


if __name__ == '__main__':

	query = raw_input('> ')

	parse(query)