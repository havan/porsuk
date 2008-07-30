#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ekrem SEREN
# Licensed under the terms of CC Attribution-NonCommercial-ShareAlike 3.0 (CC ByNcSa3)
# See: http://creativecommons.org/licenses/by-nc-sa/3.0/
# 09-12-2007
#
# Coded with Wing IDE v3 with pleasure.
# http://wingware.com/

import os, platform

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

USER_HOME = os.environ.get('HOME')

### PERSONAL SETTINGS ###
# Get node name #
PLATFORM_NODE = platform.node()

### Ekrem SEREN ########################################################
if PLATFORM_NODE == "galactica":
    DOCUMENT_ROOT = "%s/Pardus/svn/sudrap/projects/porsuk" % USER_HOME
    WEB_URL = "http://localhost:8000"

    # Database
    # 0 for Postgres
    # 1 for Sqlite3
    CHOOSE_DATABASE = 0

    if CHOOSE_DATABASE == 0:
        DATABASE_ENGINE = 'postgresql_psycopg2'
        DATABASE_NAME = 'porsuk'
        DATABASE_USER = 'porsuk'
        DATABASE_PASSWORD = 'porsuk'
        DATABASE_HOST = ''
        DATABASE_PORT = ''
    elif CHOOSE_DATABASE == 1:
        DATABASE_ENGINE = 'sqlite3'
        DATABASE_NAME = '%s/db/porsuk.db' % DOCUMENT_ROOT
        DATABASE_USER = ''
        DATABASE_PASSWORD = ''
        DATABASE_HOST = ''
        DATABASE_PORT = ''

### Mümin SEREN ########################################################
elif PLATFORM_NODE == "havan-delen":
    DOCUMENT_ROOT = "D:/thief/GRAPHIC DESIGN/SVN/porsuk/"
    WEB_URL = "http://localhost:8000"

    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = '%s/db/porsuk.db' % DOCUMENT_ROOT
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_HOST = ''
    DATABASE_PORT = ''

### Cubik Server ########################################################
elif PLATFORM_NODE == "cubikserver":
    DOCUMENT_ROOT = "/home/porsuk/svn/porsuk/"
    WEB_URL = "http://pardus.cu.edu.tr/"

    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'porsuk'
    DATABASE_USER = 'porsuk'
    DATABASE_PASSWORD = 'porsuk'
    DATABASE_HOST = ''
    DATABASE_PORT = ''

### UT.NET Server ########################################################
elif PLATFORM_NODE == "ceviz":
    DOCUMENT_ROOT = "/root/porsuk/porsuk/"
    WEB_URL = "http://uygunteknoloji.net/porsuk"

    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'porsuk'
    DATABASE_USER = 'porsuk'
    DATABASE_PASSWORD = 'xxxxxxxx'
    DATABASE_HOST = ''
    DATABASE_PORT = ''

### Ahmet Erdoğan ############################################################
elif PLATFORM_NODE == "tuxland":
    DOCUMENT_ROOT = "%s/porsuk-svn/sudrap/projects/porsuk" % USER_HOME
    WEB_URL = "http://localhost:8000"

    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'porsuk'
    DATABASE_USER = 'porsuk'
    DATABASE_PASSWORD = 'porsuk'
    DATABASE_HOST = ''
    DATABASE_PORT = ''

else:
    DOCUMENT_ROOT = "."
    WEB_URL = "http://localhost:8000"

    # Database #
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = '%s/db/porsuk.db' % DOCUMENT_ROOT
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_HOST = ''
    DATABASE_PORT = ''

########################################################################

### Porsuk Settings ###
# Prefix of package url, do not use leading slash
PACKAGE_PREFIX = "pisi/package"

# Languages choices for sum&desc
LANG_CHOICES = (('tr', 'Türkçe'),
                ('en', 'English'),
                ('it', 'Italiano'),
                ('br', 'Brazilian'),
                ('fr', 'French'),
                )

# IsA field choices
ISA_CHOICES = (('app', 'app'),
               ('app:console', 'app:console'),
               ('app:gui', 'app:gui'),
               ('app:web', 'app:web'),
               ('library', 'library'),
               ('service', 'service'),
               ('data', 'data'),
               ('data:doc','data:doc'),
               ('data:font','data:font'),
               ('kernel','kernel'),
               ('driver','driver'),
               ('locale','locale'),
               ('locale:tr','locale:tr'),
               ('locale:en','locale:en'),
               ('locale:es','locale:es'),
               ('locale:nl','locale:nl'),
               ('locale:fr','locale:fr'),
               ('locale:de','locale:de'),
               ('locale:it','locale:it'),
               )

# Pagination
PACKAGES_PER_PAGE = 50

###########################################################

### Django Settings ###
# Misc
TIME_ZONE = 'Europe/Istanbul'
#LANGUAGE_CODE = 'tr'
SITE_ID = 1
USE_I18N = True

# Media
MEDIA_ROOT = '%s/static/' % DOCUMENT_ROOT
MEDIA_URL = '%s/static/' % WEB_URL
ADMIN_MEDIA_PREFIX = '/admin_media/'

SECRET_KEY = '^9yrv)v)i^)ihdd7xyg2ng_j$7f54f9^x2o3+%nw2#&+)1d4x&'

# Template loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# Middlewares
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# Urls
ROOT_URLCONF = 'porsuk.urls'

# Templates
TEMPLATE_DIRS = ('%s/templates' % DOCUMENT_ROOT,
             )

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'porsuk.pak',
)
