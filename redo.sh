#!/bin/bash

pelican -s pelicanconf.py
cp -R output/* ~/webapps/relurori_docpad/
