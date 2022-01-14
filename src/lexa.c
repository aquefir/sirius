/****************************************************************************\
 *                                Sirius™ C*                                *
 *                                                                          *
 *                      Copyright © 2020-2021 Aquefir.                      *
 *                 Released under Artisan Software Licence.                 *
\****************************************************************************/

enum
{
	LEXEME_MALFORMED,
	LEXEME_EOF,
	LEXEME_WHITESPACE,
	LEXEME_IDENTIFIER,
	LEXEME_KEYWORD,
	LEXEME_OPERATOR,
	LEXEME_RUNE_LITERAL,
	LEXEME_UNISTRING_LITERAL,
	LEXEME_CHAR_LITERAL,
	LEXEME_STRING_LITERAL,
	LEXEME_NUMERIC_LITERAL,
	MAX_LEXEME
};

struct lexeme
{
	unsigned type;
	char * value;
};

struct lexeme_opt
{
	unsigned char is;
	struct lexeme lexeme;
	unsigned count;
};

struct state
{
	unsigned index;
};

static const char * const keywords[] = {
	"bit", "break", "case", "const", "continue", "default", "do", "else",
	"enum", "extern", "for", "goto", "if", "law", "marshal", "noalloc",
	"noreturn", "pure", "register", "return", "sizeof", "struct", "switch",
	"typedef", "union", "volatile", "while"
};

static const char * const operators[] = {
	">>>=", ">>=", "<<=", "||=", "|=", "&&=", "&=", "*=", "^^=", "^=",
	"+=", "-=", "/=", "%=", "~=", "<=", ">=", "!=", "==", "=", ">>>", ">>",
	"<<", "||", "|", "&&", "&", "*", "^^", "^", "++", "+", "--", "-",
	"/", "%", "~", "<", ">", "!", "...", ".", "?", ",", ";", ":", "(", ")",
	"[", "]", "{", "}"
};

static int is_xdigit( char c )
{
	return ( c >= '0' && c <= '9' ) || ( c >= 'A' && c <= 'F' )
		|| ( c >= 'a' && c <= 'f' );
}

static int is_odigit( char c )
{
	return c >= '0' && c <= '7';
}

static int is_digit( char c )
{
	return c >= '0' && c <= '9';
}

static int is_nzdigit( char c )
{
	return c >= '1' && c <= '9';
}

static int is_1to3( char c )
{
	return c >= '1' && c <= '3';
}

static int is_identst( char c )
{
	return ( c >= 'A' && c <= 'Z' ) || ( c >= 'a' && c <= 'z' )
		|| c == '_';
}

static int is_identch( char c )
{
	return is_identst( c ) || is_digit( c );
}

static int is_eofch( char c )
{
	return c == '\0' || c == '\032';
}

static int is_newline( char c )
{
	return c == '\n' || c == '\r';
}

static int is_wspace( char c )
{
	return c == ' ' || c == '\f' || c == '\t' || c == '\v';
}
