#!/bin/sh
# -*- coding: utf-8 -*-
##############################################################################
##                                Sirius™ C*                                ##
##                                                                          ##
##                      Copyright © 2020-2021 Aquefir.                      ##
##                 Released under Artisan Software Licence.                 ##
##############################################################################

cd doc;
echo '::: Running initial LaTeX build...';
xelatex cstar.tex;
echo '::: Rerunning build for ToC...';
xelatex cstar.tex;
echo '::: Complete. Removing intermediate files...';
rm cstar.aux cstar.log cstar.out cstar.toc;
cd ..;
