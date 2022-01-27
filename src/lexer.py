#!/opt/aq/bin/natpython
# -*- coding: ascii -*-
##############################################################################
##                                Sirius  C*                                ##
##                                                                          ##
##                     Copyright (C) 2020-2022 Aquefir.                     ##
##                 Released under Artisan Software Licence.                 ##
##############################################################################

K_KEYWORDS = [
	'break', 'case', 'const', 'continue', 'default', 'do', 'else', 'enum',
	'extern', 'for', 'goto', 'if', 'law', 'marshal', 'noreturn', 'pure',
	'register', 'return', 'sizeof', 'struct', 'switch', 'typedef', 'union',
	'volatile', 'while'
]
K_KEYWORDS_SZ = len(K_KEYWORDS)

K_OPERATORS = [
	'>>>=', '>>=', '<<<=', '<<=', '||=', '|=', '&&=', '&=', '*=', '^^=', '^=',
	'+=', '-=', '/=', '%=', '~=', '<=', '>=', '!=', '==', '=', '>>>', '>>',
	'<<<', '<<', '||', '|', '&&', '&', '*', '^^', '^', '++', '+', '--', '-',
	'/', '%', '~', '<', '>', '!', '...', '.', '?', ',', ';', ':', '(', ')',
	'[', ']', '{', '}'
]
K_OPERATORS_SZ = len(K_OPERATORS)

LEXEME_MALFORMED = 0
LEXEME_EOF = 1
LEXEME_WHITESPACE = 2
LEXEME_IDENTIFIER = 3
LEXEME_KEYWORD = 4
LEXEME_OPERATOR = 5
LEXEME_CHARLITERAL = 6
LEXEME_RUNELITERAL = 7
LEXEME_STRINGLITERAL = 8
LEXEME_UNISTRINGLITERAL = 9
LEXEME_DECLITERAL = 10 # base 10, "decimal"
LEXEME_BINLITERAL2 = 11 # base 2, "binary"
LEXEME_OCTLITERAL8 = 12 # base 8, "octal"
LEXEME_HEXLITERAL16 = 13 # base 16, "hexadecimal"
MAX_LEXEME = 14

def check_eof(text, index):
	return {
		'hit': index >= len(text) or \
			text[index] == '\u0000' or \
			text[index] == '\u001A',
		'lexeme': (LEXEME_EOF, ''),
		'count': 0
	}

def check_whitespace(text, index):
	def wspace(c):
		return c == ' ' or c == '\v' or c == '\t' or c == '\v'
	count = 0
	sz = len(text)
	while index + count < sz and wspace(text[index + count]):
		count += 1
	return {
		'hit': count > 0,
		'lexeme': (LEXEME_WHITESPACE, text[index:index + count]),
		'count': count
	}

def check_operator(text, index):
	ret = {
		'hit': False,
		'lexeme': (LEXEME_OPERATOR, ''),
		'count': 0
	}
	i = 0
	text_sz = len(text)
	while i < K_OPERATORS_SZ:
		match = True
		sz = len(K_OPERATORS[i])
		# Check to make sure we can inspect the whole operator
		if index + sz >= text_sz:
			match = False
		j = 0
		while match and j < sz:
			if text[index + j] != K_OPERATORS[i][j]:
				match = False
			j += 1
		if match:
			ret['hit'] = True
			ret['lexeme'][1] = K_OPERATORS[i]
			ret['count'] = sz
			break
		i += 1
	return ret

def check_numeric_literal(text, index):
	def bindigit(c):
		return c == '0' or c == '1'
	def digit(c):
		n = ord(c)
		return n >= 0x30 and n <= 0x39
	def hexdigit(c):
		n = ord(c)
		return digit(c) or \
			(n >= 0x41 and n <= 0x5A) or \
			(n >= 0x61 and n <= 0x7A)
	text_sz = len(text)
	ret = {
		'hit': False,
		'lexeme': (LEXEME_MALFORMED, ''),
		'count': 0
	}
	count = 0
	if text[index] == '0':
		count += 1
		if index + 1 >= text_sz:
			ret['hit'] = True
			ret['lexeme'][0] = LEXEME_OCTLITERAL
			ret['lexeme'][1] = '0'
			ret['count'] = count
			return ret
		elif text[index + 1].lower() == 'x':
			count += 1
			# save this to make sure we don't have "0x" (invalid)
			old_count = count
			while index + count < text_sz and is hexdigit(text[index + count]):
				count += 1
			if count > old_count:
				ret['lexeme'][0] = LEXEME_HEXLITERAL
			ret['hit'] = True
			ret['lexeme'][1] = text[index:index + count]
			ret['count'] = count
			return ret
		elif text[index + 1].lower() == 'b':
			count += 1
			# same logic as before with hex literals
			old_count = count
			while index + count < text_sz and is bindigit(text[index + count]):
				count += 1
			if count > old_count:
				ret['lexeme'][0] = LEXEME_BINLITERAL
			ret['hit'] = True
			ret['lexeme'][1] = text[index:index + count]
			ret['count'] = count
			return ret
		elif digit(text[index + 1]):
			count += 1
			while index + count < text_sz and is digit(text[index + count]):
				count += 1
			ret['hit'] = True
			ret['lexeme'][0] = LEXEME_OCTLITERAL
			ret['lexeme'][1] = text[index:index + count]
			ret['count'] = count
		elif text[index + 1] == '.':
			# floating-point literals

def main(args):
	print('Good morning, Vietnam!')
	return 0

if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
