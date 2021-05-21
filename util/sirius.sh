#!/bin/sh
# -*- coding: utf-8 -*-

if [ ! -d node_modules ] \
|| [ ! -d node_modules/.bin ] \
|| [ ! -f node_modules/.bin/ts-node ]; then
	echo 'ts-node wrapper script not found. please run ‘npm i’.' >/dev/stderr;
	exit 127;
fi

node_modules/.bin/ts-node src/main.ts $*
