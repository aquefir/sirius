/****************************************************************************\
 *                                Sirius™ C*                                *
 *                                                                          *
 *                      Copyright © 2020-2021 Aquefir.                      *
 *                 Released under Artisan Software Licence.                 *
\****************************************************************************/

'use strict'

export enum LexemeType {
	Malformed,
	EndOfFile,
	Whitespace,
	Identifier,
	Keyword,
	Operator,
	CharLiteral,
	RuneLiteral,
	AsciistringLiteral,
	UnistringLiteral,
	NumericLiteral
}

export interface Lexeme {
	type: LexemeType
	value: string
}

interface State {
	index: number
}

const keywords: string[] = [
	'bit', 'break', 'case', 'const', 'continue', 'default', 'do', 'else',
	'enum', 'extern', 'for', 'goto', 'if', 'law', 'marshal', 'noalloc',
	'noreturn', 'pure', 'register', 'return', 'sizeof', 'struct', 'switch',
	'typedef', 'union', 'volatile', 'while'
]

const operators: string[] = [
	'>>>=', '>>=', '<<=', '||=', '|=', '&&=', '&=', '*=', '^^=', '^=',
	'+=', '-=', '/=', '%=', '~=', '<=', '>=', '!=', '==', '=', '>>>', '>>',
	'<<', '||', '|', '&&', '&', '*', '^^', '^', '++', '+', '--', '-',
	'/', '%', '~', '<', '>', '!', '...', '.', '?', ',', ';', ':', '(', ')',
	'[', ']', '{', '}'
]

const exprHexDigit: RegExp = /^[A-Fa-f0-9]$/
const exprOctDigit: RegExp = /^[0-7]$/
const exprDecDigit: RegExp = /^[0-9]$/
const expr1to9: RegExp = /^[1-9]$/
const expr1to3: RegExp = /^[1-3]$/
const exprIdentStart: RegExp = /^[A-Za-z_]$/
const exprIdentChar: RegExp = /^[A-Za-z0-9_]$/
const exprWhitespace: RegExp = /^[\s]$/

const makeLexeme = (type: LexemeType, value: string): Lexeme => {
	return {type, value}
}

interface LexemeOption {
	hit: boolean
	lexeme: Lexeme
	count: number
}

const checkEOF = (input: string, state: State): LexemeOption => {
	return {
		hit: state.index >= input.length || input[state.index] === '\u0000'
			|| input[state.index] === '\u001A',
		lexeme: makeLexeme(LexemeType.EndOfFile, ''),
		count: 0
	}
}

const checkWhitespace = (input: string, state: State): LexemeOption => {
	let count = 0
	while(exprWhitespace.test(input[state.index + count])) {
		count++
	}
	return {
		hit: count > 0,
		lexeme: makeLexeme(LexemeType.Whitespace,
			count === 0 ? '' : input.slice(state.index, state.index + count)),
		count
	}	
}

const checkOperator = (input: string, state: State): LexemeOption => {
	for(let i = 0; i < operators.length; ++i) {
		let match: boolean = true
		for(let j = 0; state.index + j < input.length
		&& j < operators[i].length; ++j) {
			if(input[state.index + j] !== operators[i][j]) {
				match = false
				break
			}
		}
		if(match) {
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.Operator, operators[i]),
				count: operators[i].length
			}
		}
		// if no match, keep going and eventually quit
	}
	return {
		hit: false,
		lexeme: makeLexeme(LexemeType.Operator, ''),
		count: 0
	}
}

const checkHexadecimalLiteral = (input: string, state: State):
LexemeOption => {
	// ASSUME: input at index is “0x” or “0X”
	let count = 2
	while(exprHexDigit.test(input[state.index + count])) {
		count++
	}
	return {
		hit: count > 2,
		lexeme: makeLexeme(count > 2 ? LexemeType.NumericLiteral :
			LexemeType.Malformed,
			input.slice(state.index, state.index + count)),
		count
	}
}

const checkNumericLiteral = (input: string, state: State): LexemeOption => {
	if(input[state.index] === '0') {
		if(state.index + 1 >= input.length) {
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.NumericLiteral, '0'),
				count: 1
			}
		}
		// hexadecimal
		if(input[state.index + 1] === 'X' || input[state.index + 1] === 'x') {
			const lexemeOpt = checkHexadecimalLiteral(input, state)
			if(lexemeOpt.hit) {
				return lexemeOpt
			}
		}
	} else if(expr1to9.test(input[state.index])) {
		let count = 1
		while(exprDecDigit.test(input[state.index + count])) {
			count++
		}
		return {
			hit: true,
			lexeme: makeLexeme(LexemeType.NumericLiteral,
				input.slice(state.index, state.index + count)),
			count
		}
	}
	return {
		hit: false,
		lexeme: makeLexeme(LexemeType.NumericLiteral, ''),
		count: 0
	}
}

const checkKeyword = (input: string, state: State): LexemeOption => {
	for(let i = 0; i < keywords.length; ++i) {
		let match = true
		for(let j = 0; state.index + j < input.length
		&& j < keywords[i].length; ++j) {
			if(input[state.index + j] !== keywords[i][j]) {
				match = false
				break
			}
		}
		if(match) {
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.Keyword, keywords[i]),
				count: keywords[i].length
			}
		}
		// if no match, keep going and eventually quit
	}
	return {
		hit: false,
		lexeme: makeLexeme(LexemeType.Keyword, ''),
		count: 0
	}
}

const checkIdentifier = (input: string, state: State): LexemeOption => {
	if(!exprIdentStart.test(input[state.index])) {
		return {
			hit: false,
			lexeme: makeLexeme(LexemeType.Identifier, ''),
			count: 0
		}
	}
	let count = 1
	while(count + state.index < input.length
	&& exprIdentChar.test(input[state.index + count])) {
		count++
	}
	return {
		hit: true,
		lexeme: makeLexeme(LexemeType.Identifier,
			input.slice(state.index, state.index + count)),
		count
	}
}

const escZeroLiteral = (input: string, state: State, offset: number,
type: LexemeType): LexemeOption => {
	const midIsOctal = exprOctDigit.test(input[state.index + offset + 1])
	const hit = input[state.index + offset] === '0'
		|| (exprOctDigit.test(input[state.index + offset])
		&& midIsOctal && exprOctDigit.test(input[state.index + offset + 2]))
	const count = (midIsOctal ? 3 : 1)
	return {
		hit: true,
		lexeme: makeLexeme(hit ?
			LexemeType.NumericLiteral : LexemeType.Malformed,
			input.slice(state.index + offset, state.index + offset +	count)),
		count
	}
}

const escOctLiteral = (input: string, state: State, offset: number,
type: LexemeType): LexemeOption => {
	const hit = expr1to3.test(input[state.index + offset])
		&& exprOctDigit.test(input[state.index + offset + 1])
		&& exprOctDigit.test(input[state.index + offset + 2])
	return {
		hit: true,
		lexeme: makeLexeme(hit ? LexemeType.NumericLiteral :
			LexemeType.Malformed,
			input.slice(state.index + offset, state.index + offset + 3)),
		count: 3
	}
}

const escUni16Literal = (input: string, state: State, offset: number,
type: LexemeType): LexemeOption => {
	return {
		hit: true,
		lexeme: makeLexeme(type,
			String.fromCodePoint(parseInt(input.slice(state.index + offset + 1,
			state.index + offset + 1 + 4), 16))),
		count: 1 + 4
	}
}

const escUni32Literal = (input: string, state: State, offset: number,
type: LexemeType): LexemeOption => {
	return {
		hit: true,
		lexeme: makeLexeme(type,
			String.fromCodePoint(parseInt(input.slice(state.index + offset + 1,
			state.index + offset + 1 + 8), 16))),
		count: 1 + 8
	}
}

const flatEsc = {
	'a': '\u0007',
	'b': '\u0008',
	'f': '\u000C',
	'n': '\u000A',
	'r': '\u000D',
	't': '\u0009',
	'v': '\u000B',
	'\'': '\'',
	'"': '"',
	'?': '?',
	'\\': '\\'
}

const genEscFlatFunction = (ch: string): (input: string, state: State,
offset: number, type: LexemeType) => LexemeOption => {
	return (input: string, state: State, offset: number, type: LexemeType):
	LexemeOption => {
		return {
			hit: true,
			lexeme: makeLexeme(type, flatEsc[ch]),
			count: 1
		}
	}
}

const escRuneLiteral = {
	'0': escZeroLiteral,
	'1': escOctLiteral,
	'2': escOctLiteral,
	'3': escOctLiteral,
	'a': genEscFlatFunction('a'),
	'b': genEscFlatFunction('b'),
	'f': genEscFlatFunction('f'),
	'n': genEscFlatFunction('n'),
	'r': genEscFlatFunction('r'),
	't': genEscFlatFunction('t'),
	'U': escUni16Literal,
	'u': escUni32Literal,
	'v': genEscFlatFunction('v'),
	'\'': genEscFlatFunction('\''),
	'?': genEscFlatFunction('?'),
	'\\': genEscFlatFunction('\\')
}

const escUnistringLiteral = {
	'0': escZeroLiteral,
	'1': escOctLiteral,
	'2': escOctLiteral,
	'3': escOctLiteral,
	'a': genEscFlatFunction('a'),
	'b': genEscFlatFunction('b'),
	'f': genEscFlatFunction('f'),
	'n': genEscFlatFunction('n'),
	'r': genEscFlatFunction('r'),
	't': genEscFlatFunction('t'),
	'U': escUni16Literal,
	'u': escUni32Literal,
	'v': genEscFlatFunction('v'),
	'"': genEscFlatFunction('"'),
	'?': genEscFlatFunction('?'),
	'\\': genEscFlatFunction('\\')
}

const checkRuneLiteral = (input: string, state: State): LexemeOption => {
	if(state.index + 4 >= input.length
	|| input[state.index] !== '@'
	|| input[state.index + 1] !== '\'') {
		return {
			hit: false,
			lexeme: makeLexeme(LexemeType.RuneLiteral, ''),
			count: 0
		}
	}
	if(input[state.index + 2] === '\\') {
		const code = input[state.index + 3]
		// invalid escape sequence starting character
		if(!escRuneLiteral.hasOwnProperty(code)) {
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.Malformed,
					input.slice(state.index, state.index + 4)),
				count: 4
			}
		}
		const lexemeOpt: LexemeOption =
			escRuneLiteral[code](input, state, 3, LexemeType.RuneLiteral)
		if(state.index + 3 + lexemeOpt.count >= input.length
		|| input[state.index + 3 + lexemeOpt.count] !== '\'') {
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.Malformed,
					input.slice(state.index, state.index + 3 + lexemeOpt.count)),
				count: input.length - state.index
			}
		}
		lexemeOpt.count += 3 + 1
		return lexemeOpt
	}
	// no backslashes to variate the width, so this must be a closing quote
	if(input[state.index + 3] !== '\'') {
		return {
			hit: true,
			lexeme: makeLexeme(LexemeType.Malformed,
				input.slice(state.index, state.index + 3)),
			count: 3
		}
	}
	return {
		hit: true,
		lexeme: makeLexeme(LexemeType.RuneLiteral, input[state.index + 2]),
		count: 4
	}
}

const checkUnistringLiteral = (input: string, state: State): LexemeOption => {
	if(state.index + 3 >= input.length
	|| input[state.index] !== '@'
	|| input[state.index + 1] !== '"') {
		return {
			hit: false,
			lexeme: makeLexeme(LexemeType.UnistringLiteral, ''),
			count: 0
		}
	}
	let len = 0
	let str = ''
	while(state.index + 2 + len < input.length) {
		const i = state.index + 2 + len
		if(input[i] === '\\') {
			if(i + 1 >= input.length) {
				const lexeme = input.slice(state.index, i + 1)
				return {
					hit: true,
					lexeme: makeLexeme(LexemeType.Malformed, lexeme),
					count: lexeme.length
				}
			}
			const code = input[i + 1]
			if(!escUnistringLiteral.hasOwnProperty(code)) {
				const lexeme = input.slice(state.index, i + 2)
				return {
					hit: true,
					lexeme: makeLexeme(LexemeType.Malformed, lexeme),
					count: lexeme.length
				}
			}
			const lexemeOpt: LexemeOption =
				escUnistringLiteral[code](input, state, 2 + len,
					LexemeType.UnistringLiteral)
			if(i + 1 + lexemeOpt.count >= input.length) {
				const lexeme = input.slice(state.index, i + 1 + lexemeOpt.count)
				return {
					hit: true,
					lexeme: makeLexeme(LexemeType.Malformed, lexeme),
					count: lexeme.length
				}
			}
			str += lexemeOpt.lexeme.value
			len += lexemeOpt.count
			continue
		}
		if(input[i] === '"') {
			state.index += len + 1
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.UnistringLiteral, str),
				count: str.length
			}
		}
		const cp0 = input[i].codePointAt(0)
		if(cp0 < 0x20 || cp0 > 0x7F) {
			const lexeme = input.slice(state.index, i)
			return {
				hit: true,
				lexeme: makeLexeme(LexemeType.Malformed, lexeme),
				count: lexeme.length
			}
		}
		str += input[i]
		len++
	}
	// No terminating double-quote, therefore Malformed
	const lexeme = input.slice(state.index, state.index + 2 + len)
	return {
		hit: true,
		lexeme: makeLexeme(LexemeType.Malformed, lexeme),
		count: lexeme.length
	}
}

type CheckerFunction = (input: string, state: State) => LexemeOption

const checkers: CheckerFunction[] = [
	checkEOF,
	checkWhitespace,
	checkOperator,
	checkNumericLiteral,
	checkKeyword,
	checkIdentifier,
	checkRuneLiteral,
	checkUnistringLiteral
]

export const lexemeToString = (input: Lexeme): string => {
	return '{type:' + LexemeType[input.type] + ',value:"' + input.value.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t') + '"}'
}

const lex = (input: string, state: State): Lexeme => {
	for(let i = 0; i < checkers.length; ++i) {
		const opt: LexemeOption = checkers[i](input, state)
		if(opt.hit) {
			state.index += opt.count
			return opt.lexeme
		}
	}
	state.index++
	// if nothing else, keep this function robust. let the caller handle it
	return makeLexeme(LexemeType.Malformed, input[state.index - 1])
}

export const lexAll = (input: string): Lexeme[] => {
	let ret: Lexeme[] = []
	let state: State = {
		index: 0
	}
	for(;;) {
		const lexeme: Lexeme = lex(input, state)
		ret.push(lexeme)
		// above, we push the EOF Lexeme regardless
		// in C, we don’t carry length, so this can be copied thoughtlessly
		if(lexeme.type === LexemeType.EndOfFile) {
			break
		}
	}
	return ret
}
