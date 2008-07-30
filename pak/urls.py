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

from django.conf.urls.defaults import *
from porsuk.pak.views import *
from porsuk.pak.models import *
from porsuk.settings import PACKAGES_PER_PAGE
from django.shortcuts import get_object_or_404

urlpatterns = patterns('',
    (r'packages/$', "django.views.generic.simple.redirect_to", {"url": "/pisi/packages/order-by/name"}),
    (r'packages/order-by/(?P<orderby>.*)$', packages),
    (r'package/(?P<id>.*)$', package),
    (r'sources/$', "django.views.generic.simple.redirect_to", {"url": "/pisi/sources/order-by/name"}),
    (r'sources/order-by/(?P<orderby>.*)$', sources),
    (r'source/(?P<id>.*)/$', source),
    (r'repositories/$', "django.views.generic.simple.redirect_to", {"url": "/pisi/repositories/order-by/name"}),
    (r'repositories/order-by/(?P<orderby>.*)$', repositories),
    (r'repository/(?P<repo>.*)/(?P<type>.*)$', repository),
    (r'packagers/$',  "django.views.generic.simple.redirect_to", {"url": "/pisi/packagers/order-by/name"}),
    (r'packagers/order-by/(?P<orderby>.*)$', packagers),
    (r'packager/(?P<name>.*)/(?P<type>.*)$', packager_info),
    (r'packager/(?P<name>.*)$', packager),
    (r'updates/$',  "django.views.generic.simple.redirect_to", {"url": "/pisi/updates/order-by/-date"}),
    (r'updates/type/(?P<type>.*)$', updates),
    (r'updates/order-by/(?P<orderby>.*)$', updates),
    (r'update/(?P<id>.*)$', update),
    (r'search/(?P<pattern>.*)$', search),
)
