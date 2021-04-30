/****************************************************************************\
 *                                Sirius™ C*                                *
 *                                                                          *
 *                      Copyright © 2020-2021 Aquefir.                      *
 *                 Released under Artisan Software Licence.                 *
\****************************************************************************/

'use strict'

const main = (args: string[]): number => {
	console.log(args)
	return 0
}

if(require.main === module) {
	process.exit(main(process.argv.slice(1)))
}
