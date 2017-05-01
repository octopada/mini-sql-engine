import sqlparse
from sqlparse import tokens

class Parser:

	@classmethod
	def process_query(cls, query, database):

		parsed_query = sqlparse.parse(query)
		query_tokens = parsed_query[0].tokens

		if query_tokens[0].match(tokens.DML, '.*', regex = True):

			statement_data = cls.link_to_parser(query_tokens)

		else:

			raise SyntaxError('Invalid query')

		return statement_data


	@classmethod
	def link_to_parser(cls, query_tokens):

		if query_tokens[0].match(tokens.DML, 'SELECT'):

			statement_data = cls.parse_select(query_tokens)

		else:

			raise NotImplementedError('DML statement not implemented')

		return statement_data


	@classmethod
	def parse_select(cls, query_tokens):

		token_it = 0
		statement_data = {'command': 'SELECT', 'has_where': False, 'has_function': False}

		try:

			select_clause, token_it = Parser.get_next_token(query_tokens, token_it)

			# handle DISTINCT
			next_token, token_it = Parser.get_next_token(query_tokens, token_it) 
			if next_token.match(tokens.Keyword, 'DISTINCT'):

				statement_data['distinct'] = True
				column_identifiers, token_it = Parser.get_next_token(query_tokens, token_it)

			else:

				statement_data['distinct'] = False
				column_identifiers = next_token

			from_clause, token_it = Parser.get_next_token(query_tokens, token_it)
			table_identifiers, token_it = Parser.get_next_token(query_tokens, token_it)

		except IndexError:

			raise IndexError('Invalid select statement')

		column_id_string = column_identifiers.value
		column_id_list = Parser.get_list_from_string(column_id_string, ',')
		statement_data['column_ids'] = column_id_list

		table_id_string = table_identifiers.value
		table_id_list = Parser.get_list_from_string(table_id_string, ',')
		statement_data['table_ids'] = table_id_list

		statement_data = Parser.check_functions(statement_data)

		backup_token_it = token_it
		try:

			where_clause, token_it = Parser.get_next_token(query_tokens, token_it)

			if not where_clause.match(None, 'WHERE .*', regex = True):

				token_it = backup_token_it

			else:

				statement_data['has_where'] = True
				where_clause_string = where_clause.value
				where_clause_list = Parser.get_list_from_string(where_clause_string, ' ')
				statement_data['where_clause'] = where_clause_list[1:]

		except IndexError:

			return statement_data

		return statement_data


	@staticmethod
	def get_list_from_string(string, split_by):

		ret = string.split(split_by)

		for word_it in range(len(ret)):

			ret[word_it] = ret[word_it].strip()

		return ret


	@staticmethod
	def get_next_token(query_tokens, token_it):

		token = query_tokens[token_it]
		token_it += 2

		return token, token_it


	@staticmethod
	def check_functions(statement_data):

		column_id_list = statement_data['column_ids']

		try:

			function, column = column_id_list[0].split('(')
			column = column.split(')')
			column = column[0]
			column_id_list[0] = column

			if function == 'distinct':

				statement_data['distinct'] = True

			else:

				statement_data['has_function'] = True
				statement_data['function'] = function
				statement_data['function_column'] = column

		except ValueError:

			return statement_data

		return statement_data