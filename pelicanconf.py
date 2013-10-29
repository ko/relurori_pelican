#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ken Ko'
SITENAME = u'notes for myself'
SITEURL = 'http://relurori.com'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),
          )

# Social widget
SOCIAL = (('github', 'http://github.com/ko'),
        ('LinkedIn', 'http://linkedin.com/in/kenko'),
        ('flickr', 'http://flickr.com/photos/yaksok'),
        )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "./pelican-themes/sundown"
THEME = "./pelican-themes/bootlex"
THEME = "./pelican-themes/built-texts"
THEME = "./pelican-themes/tuxlite_zf"
