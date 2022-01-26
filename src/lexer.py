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

K_OPERATORS = [
	'>>>=', '>>=', '<<<=', '<<=', '||=', '|=', '&&=', '&=', '*=', '^^=', '^=',
	'+=', '-=', '/=', '%=', '~=', '<=', '>=', '!=', '==', '=', '>>>', '>>',
	'<<<', '<<', '||', '|', '&&', '&', '*', '^^', '^', '++', '+', '--', '-',
	'/', '%', '~', '<', '>', '!', '...', '.', '?', ',', ';', ':', '(', ')',
	'[', ']', '{', '}'
]

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
LEXEME_NUMERICLITERAL = 10
MAX_LEXEME = 11

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

def main(args):
	print('Good morning, Vietnam!')
	return 0

if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
