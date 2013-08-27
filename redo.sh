#!/bin/bash

#pelican -s pelicanconf.py -t `pwd`/pelican-themes/mnmlist
make html
cp -R output/* ~/webapps/relurori_docpad/
