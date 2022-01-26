/****************************************************************************\
 *                                Sirius  C*                                *
 *                                                                          *
 *                     Copyright (C) 2020-2022 Aquefir.                     *
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

enum
{
	KEYWORD_BIT,
	KEYWORD_BREAK,
	KEYWORD_CASE,
	KEYWORD_CONST,
	KEYWORD_CONTINUE,
	KEYWORD_DEFAULT,
	KEYWORD_DO,
	KEYWORD_ELSE,
	KEYWORD_ENUM,
	KEYWORD_EXTERN,
	KEYWORD_FOR,
	KEYWORD_GOTO,
	KEYWORD_IF,
	KEYWORD_LAW,
	KEYWORD_MARSHAL,
	KEYWORD_NORETURN,
	KEYWORD_PURE,
	KEYWORD_REGISTER,
	KEYWORD_RETURN,
	KEYWORD_SIZEOF,
	KEYWORD_STRUCT,
	KEYWORD_SWITCH,
	KEYWORD_TYPEDEF,
	KEYWORD_UNION,
	KEYWORD_VOLATILE,
	KEYWORD_WHILE,
	MAX_KEYWORD
};

enum
{
	OP_SIGNED_RSHIFT_SET,
	OP_RSHIFT_SET,
	OP_ROTATE_LEFT_SET,
	OP_LSHIFT_SET,
	OP_OROR_SET,
	OP_OR_SET,
	OP_ANDAND_SET,
	OP_AND_SET,
	OP_MUL_SET,
	OP_POW_SET,
	OP_XOR_SET,
	OP_PLUS_SET,
	OP_MINUS_SET,
	OP_DIV_SET,
	OP_MOD_SET,
	OP_BITNOT_SET,
	OP_LE,
	OP_GE,
	OP_NOTEQUALTO,
	OP_EQUALTO,
	OP_SET,
	OP_SIGNED_RSHIFT,
	OP_RSHIFT,
	OP_ROTATE_LEFT,
	OP_LSHIFT,
	OP_OROR,
	OP_OR,
	OP_ANDAND,
	OP_AND,
	OP_MUL,
	OP_POW,
	OP_XOR,
	OP_PLUSPLUS,
	OP_PLUS,
	OP_MINUSMINUS,
	OP_MINUS,
	OP_DIV,
	OP_MOD,
	OP_BITNOT,
	OP_LT,
	OP_GT,
	OP_NOT,
	OP_DOTDOTDOT,
	OP_DOT,
	OP_QUESTION,
	OP_COMMA,
	OP_SEMICOLON,
	OP_COLON,
	OP_LPAREN,
	OP_RPAREN,
	OP_LBRACK,
	OP_RBRACK,
	OP_LBRACE,
	OP_RBRACE,
	MAX_OP
};

struct lexeme
{
	unsigned type;
	unsigned value_sz;
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
	"enum", "extern", "for", "goto", "if", "law", "marshal", "noreturn",
	"pure", "register", "return", "sizeof", "struct", "switch", "typedef",
	"union", "volatile", "while"
};

static const char * const operators[] = {
	">>>=", ">>=", "<<<=", "<<=", "||=", "|=", "&&=", "&=", "*=", "^^=", "^=",
	"+=", "-=", "/=", "%=", "~=", "<=", ">=", "!=", "==", "=", ">>>", ">>",
	"<<<", "<<", "||", "|", "&&", "&", "*", "^^", "^", "++", "+", "--", "-",
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

static struct lexeme_opt check_eof( const char * input, unsigned input_sz, struct state * state )
{
	const struct lexeme lexeme = {
		LEXEME_EOF,
		1,
		&(input[state->index])
	};
	const struct lexeme_opt ret = {
		state->index >= input_sz || input[state->index] == 0x00
			|| input[state->index] == 0x1A,
		lexeme,
		0
	};

	return ret;
}

static struct lexeme_opt check_wspace( const char * input, unsigned input_sz,
struct state * state )
{
	unsigned count = 0;

	while( state->index + count < input_sz &&
	is_wspace( input[state->index + count] ))
	{
		count++;
	}

	{
		const struct lexeme lexeme = {
			LEXEME_WHITESPACE,
			count,
			&(input[state->index])
		};
		const struct lexeme_opt ret = {
			count > 0,
			lexeme,
			count
		};

		return ret;
	}
}

static struct lexeme_opt check_operator( const char * input,
unsigned input_sz, struct state * state )
{
	struct lexeme_opt ret;

	return ret;
}
