#!/opt/aq/bin/natpython
# -*- coding: ascii -*-
##############################################################################
##                                Sirius  C*                                ##
##                                                                          ##
##                     Copyright (C) 2020-2022 Aquefir.                     ##
##                 Released under Artisan Software Licence.                 ##
##############################################################################

K_FUNDPRIMS = ['bit', 'void']
K_FUNDPRIMS_SZ = len(K_FUNDPRIMS)

K_STRMODS = ['const', 'extern', 'register', 'volatile']
K_STRMODS_SZ = len(K_STRMODS)

K_FNMODS = ['noreturn', 'pure']
K_FNMODS_SZ = len(K_FNMODS)

K_KEYWORDS = [
	'break', 'case', 'continue', 'default', 'do', 'else', 'enum', 'for',
	'goto', 'if', 'law', 'marshal', 'return', 'sizeof', 'struct', 'switch',
	'typedef', 'union', 'while'
]
K_KEYWORDS_SZ = len(K_KEYWORDS)

K_LITERALPREFIXES = ['0x', '0b', '0']
K_LITERALPREFIXES_SZ = len(K_LITERALPREFIXES)

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
LEXEME_BINLITERAL = 11 # base 2, "binary"
LEXEME_OCTLITERAL = 12 # base 8, "octal"
LEXEME_HEXLITERAL = 13 # base 16, "hexadecimal"
LEXEME_FLOATLITERAL = 14 # floating-point literal
MAX_LEXEME = 15

def check_eof(text, index):
	return {
		'hit': index >= len(text) or \
			text[index] == '\u0000' or \
			text[index] == '\u001A',
		'type': LEXEME_EOF,
		'data': ''
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
		'type': LEXEME_WHITESPACE,
		'data': text[index:index + count]
	}

def check_keyword(text, index):
	ret = {
		'hit': False,
		'type': LEXEME_OPERATOR,
		'data': 0
	}
	i = 0
	text_sz = len(text)
	while i < K_KEYWORDS_SZ:
		match = True
		sz = len(K_KEYWORDS[i])
		# check to make sure we can inspect the whole keyword
		if index + sz >= text_sz:
			match = False
		j = 0
		# now check the chars of the keyword
		while match and j < sz:
			if text[index + j] != K_KEYWORDS[i][j]:
				match = False
				break
			j += 1
		if match:
			ret['hit'] = True
			ret['data'] = K_KEYWORDS[i]
			break
		i += 1
	return ret

def check_operator(text, index):
	ret = {
		'hit': False,
		'type': LEXEME_OPERATOR,
		'data': ''
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
		# now check the chars of the operator
		while match and j < sz:
			if text[index + j] != K_OPERATORS[i][j]:
				match = False
				break
			j += 1
		if match:
			ret['hit'] = True
			ret['data'] = K_OPERATORS[i]
			break
		i += 1
	return ret

def check_identifier(text, index):
	def identstart(c):
		n = ord(c)
		return (n >= ord('A') and n <= ord('Z')) or \
			(n >= ord('a') and n <= ord('z')) or c == '_'
	def digit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('9')
	ret = {
		'hit': False,
		'type': LEXEME_IDENTIFIER,
		'data': ''
	}
	if not identstart(text[index]):
		return ret
	text_sz = len(text)
	count = 1
	while index + count < text_sz:
		c = text[index + count]
		if identstart(c) or digit(c):
			count += 1
		else: break
	ret['hit'] = True
	ret['data'] = text[index:index + count]

def check_numeric_literal_float(text, index):
	def digit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('9')
	def letter(c):
		n = ord(c)
		return (n >= ord('A') and n <= ord('Z')) or \
			(n >= ord('a') and n <= ord('z'))
	text_sz = len(text)
	ret = {
		'hit': False,
		'type': LEXEME_FLOATLITERAL,
		'data': ''
	}
	dot = False
	suffix = False
	count = 0
	while index + count < text_sz:
		if digit(text[index]):
			if suffix:
				ret['hit'] = True
				ret['type'] = LEXEME_MALFORMED
				ret['data'] = text[index:index + count]
				return ret
			count += 1
		elif text[index] == '.':
			if count == 0:
				return ret
			elif dot == False:
				dot = True
				count += 1
			else:
				ret['hit'] = True
				ret['type'] = LEXEME_MALFORMED
				ret['data'] = text[index:index + count]
				return ret
		elif letter(text[index]):
			suffix = True
			count += 1
		elif count > 0:
			if dot:
				ret['hit'] = True
			ret['data'] = text[index:index + count]
			return ret
		else:
			return ret
	return ret

def check_numeric_literal_bin(text, index):
	def bindigit(c):
		return c == '0' or c == '1'
	ret = {
		'hit': False,
		'type': LEXEME_BINLITERAL,
		'data': ''
	}
	text_sz = len(text)
	if index + 2 >= text_sz or text[index:index + 2] != '0b':
		return ret
	count = 0
	while index + 2 + count + 2 < text_sz:
		if bindigit(text[index + 2 + count]):
			count += 1
		else:
			break
	ret['hit'] = True
	if count == 0:
		ret['type'] = LEXEME_MALFORMED
	ret['data'] = text[index:index + 2 + count]
	return ret

def check_numeric_literal_hex(text, index):
	def hexdigit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('9') or \
			(n >= ord('a') and n <= ord('f')) or \
			(n >= ord('A') and n <= ord('F'))
	ret = {
		'hit': False,
		'type': LEXEME_HEXLITERAL,
		'data': ''
	}
	text_sz = len(text)
	if index + 2 >= text_sz or text[index:index + 2] != '0x':
		return ret
	count = 0
	while index + 2 + count < text_sz:
		if hexdigit(text[index + 2 + count]):
			count += 1
		else: break
	ret['hit'] = True
	if count == 0:
		ret['type'] = LEXEME_MALFORMED
	ret['data'] = text[index:index + 2 + count]
	return ret

def check_numeric_literal_oct(text, index):
	def octdigit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('7')
	ret = {
		'hit': False,
		'type': LEXEME_OCTLITERAL,
		'data': ''
	}
	text_sz = len(text)
	if index + 1 >= text_sz or text[index] != '0':
		return ret
	count = 1
	while index + count < text_sz:
		if octdigit(text[index + count]):
			count += 1
		else: break
	ret['hit'] = True
	ret['data'] = text[index:index + count]
	return ret

def check_numeric_literal_dec(text, index):
	def nzdigit(c):
		n = ord(c)
		return n >= ord('1') and n <= ord('9')
	ret = {
		'hit': False,
		'type': LEXEME_DECLITERAL,
		'data': ''
	}
	text_sz = len(text)
	if not nzdigit(text[index]):
		return ret
	count = 1
	while index + count < text_sz:
		c = text[index + count]
		if nzdigit(c) or c == '0':
			count += 1
		else: break
	ret['hit'] = True
	ret['data'] = text[index:index + count]
	return ret

def check_char_literal(text, index):
	def leadoctdigit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('3')
	def octdigit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('7')
	ret = {
		'hit': False,
		'type': LEXEME_CHARLITERAL,
		'data': ''
	}
	text_sz = len(text)
	if text[index] != "'":
		return ret
	ret['hit'] = True
	if text[index + 1] == '\\':
		if index + 3 >= text_sz:
			ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 1]
			return ret
		if text[index + 2] == '\\' or text[index + 2] == "'":
			if text[index + 3] != "'":
				ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 4]
			return ret
		elif leadoctdigit(c1):
			if index + 5 >= text_sz:
				ret['type'] = LEXEME_MALFORMED
				ret['data'] = text[index:index + 3]
				return ret
			if not octdigit(text[index + 3]) or \
			not octdigit(text[index + 4]):
				ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 6]
			return ret
		else:
			ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 4]
			return ret
	elif index + 2 >= text_sz or \
	text[index + 2] != "'" or \
	ord(text[index + 1]) >= 0x7F:
		ret['type'] = LEXEME_MALFORMED
	ret['data'] = text[index:index + 3]
	return ret

def check_rune_literal(text, index):
	def hexdigit(c):
		n = ord(c)
		return n >= ord('0') and n <= ord('9') or \
			(n >= ord('a') and n <= ord('f')) or \
			(n >= ord('A') and n <= ord('F'))
	ret = {
		'hit': False,
		'type': LEXEME_RUNELITERAL,
		'data': ''
	}
	text_sz = len(text)
	if index + 1 >= text_sz or text[index:index + 1] != "@'":
		return ret
	ret['hit'] = True
	if text[index + 2] == '\\':
		if index + 4 >= text_sz:
			ret['type'] = LEXEME_MALFORMED,
			ret['data'] = text[index:index + 2]
			return ret
		if text[index + 3] == '\\' or text[index + 3] == "'":
			if text[index + 4] != "'":
				ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 5]
			return ret
		elif text[index + 3] == 'u':
			if index + 8 >= text_sz:
				ret['type'] = LEXEME_MALFORMED
				ret['data'] = text[index:index + 4]
				return ret
			if not hexdigit(text[index + 4]) or \
			not hexdigit(text[index + 5]) or \
			not hexdigit(text[index + 6]) or \
			not hexdigit(text[index + 7]):
				ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 9]
			return ret
		elif text[index + 3] == 'U':
			if index + 12 >= text_sz:
				ret['type'] = LEXEME_MALFORMED
				ret['data'] = text[index:index + 4]
				return ret
			if not hexdigit(text[index + 4]) or \
			not hexdigit(text[index + 5]) or \
			not hexdigit(text[index + 6]) or \
			not hexdigit(text[index + 7]) or \
			not hexdigit(text[index + 8]) or \
			not hexdigit(text[index + 9]) or \
			not hexdigit(text[index + 10]) or \
			not hexdigit(text[index + 11]):
				ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 13]
			return ret
		else:
			ret['type'] = LEXEME_MALFORMED
			ret['data'] = text[index:index + 5]
			return ret
	elif index + 3 >= text_sz or \
	text[index + 3] != "'" or \
	ord(text[index + 2]) >= 0x7F:
		ret['type'] = LEXEME_MALFORMED
	ret['data'] = text[index:index + 4]
	return ret

def main(args):
	print('Good morning, Vietnam!')
	return 0

if __name__ == '__main__':
	from sys import argv, exit
	exit(main(argv))
