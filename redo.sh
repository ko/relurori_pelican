#!/bin/bash

#pelican -s pelicanconf.py -t `pwd`/pelican-themes/sundown
#make regenerate
#make html
make publish
cp -R output/* ~/webapps/relurori_docpad/
