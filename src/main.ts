/****************************************************************************\
 *                                Sirius™ C*                                *
 *                                                                          *
 *                      Copyright © 2020-2021 Aquefir.                      *
 *                 Released under Artisan Software Licence.                 *
\****************************************************************************/

'use strict'

import * as FS from 'fs'
import * as Path from 'path'

import { lexAll, lexemeToString, Lexeme } from './lexa'

const kHelpText = 'Sirius™ C*\nThe brightest star in the night sky.\n\n' +
	'Copyright © 2020-2021 Aquefir.\n' +
	'Released under Artisan Software Licence.\n' +
	'\n' +
	'Usage:  sirius [options] [input [more inputs...]]\n' +
	'\n' +
	'Flags and options:-\n' +
	'    -h, --help                  show this help\n' +
	'    -o <file>, --output=<file>  file path to stream output into.\n' +
	'                                if unspecified, defaults to stdout.\n' +
	'\n' +
	'If the sole input is ‘-’, then stdin is read.\n' +
	'\n' +
	'For now, Sirius C* compiler translates C* code to ANSI C code.\n' +
	'No options are available to control the output just yet.'

type InputFile = { stdio: boolean, file: string }

const main = (args: string[]): number => {
	console.error('')
	if(args.length === 1
	|| args.indexOf('-h') !== -1
	|| args.indexOf('--help') !== -1) {
		console.error(kHelpText)
		console.error('')
		return 0
	}
	let output: string = ''
	let input: InputFile[] = []
	for(let i = 1; i < args.length; ++i) {
		if(args[i] === '-o'
		|| args[i] === '--output') {
			if(i + 1 >= args.length) {
				console.error('Hanging ‘' + args[i] + '’ argument. Exiting...')
				return 127
			}
			output = args[i + 1]
			++i
		} else if(args[i].startsWith('--output=')) {
			output = args[i].substr('--output='.length)
		} else if(args[i] === '-') {
			if(input.length > 0) {
				console.error('Cannot read stdin with other inputs. Exiting...')
				return 127
			} else {
				input.push({ stdio: true, file: 'stdin' })
			}
		} else if(args[i].startsWith('-')) {
			console.error('Unknown flag or option ‘' + args[i] + '’. Exiting...')
			return 127
		} else {
			input.push({ stdio: false, file: args[i] })
		}
	}
	let stdinRead = false
	for(let i = 0; i < input.length; ++i) {
		console.log('Reading ‘' + input[i].file + '’...')
		const lexemes: Lexeme[] = lexAll(!stdinRead && input[i].stdio ?
			process.stdin.read() : FS.readFileSync(input[i].file, 'utf8'))
		if(input[i].stdio) {
			stdinRead = true
		}
		for(let j = 0; j < lexemes.length; ++j) {
			const lexeme = lexemeToString(lexemes[j]) + '\n'
			if(output === '') {
				process.stdout.write(lexeme)
			} else {
				FS.writeFile(output, lexeme, 'utf8',
					(err: NodeJS.ErrnoException): void => {
						if(err) { console.error(err) }
					})
			}
		}
	}
	console.error('')
	return 0
}

if(require.main === module) {
	process.exit(main(process.argv.slice(1)))
}
