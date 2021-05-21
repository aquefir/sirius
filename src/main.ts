/****************************************************************************\
 *                                Sirius™ C*                                *
 *                                                                          *
 *                      Copyright © 2020-2021 Aquefir.                      *
 *                 Released under Artisan Software Licence.                 *
\****************************************************************************/

'use strict'

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

const main = (args: string[]): number => {
	if(args.indexOf('-h') !== -1
	|| args.indexOf('--help') !== -1) {
		console.error('')
		console.error(kHelpText)
		console.error('')
		return 0
	}
	const input: Buffer | null = process.stdin.read()
	if(input == null) {
		console.error('')
		console.error('No input given via stdin. Exiting...')
		console.error('')
		return 127
	}
	const lexemes: Lexeme[] = lexAll(input.toString())
	for(let j = 0; j < lexemes.length; ++j) {
		const lexeme = lexemeToString(lexemes[j]) + '\n'
		process.stdout.write(lexeme)
	}
	return 0
}

if(require.main === module) {
	process.exit(main(process.argv.slice(1)))
}
