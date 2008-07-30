#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ekrem SEREN
# Licensed under the terms of CC Attribution-NonCommercial-ShareAlike 3.0 (CC ByNcSa3)
# See: http://creativecommons.org/licenses/by-nc-sa/3.0/
#
# Coded with Wing IDE v3 with pleasure.
# http://wingware.com/

from django.conf.urls.defaults import *
from porsuk.pak.views import mainpage
from porsuk.settings import DOCUMENT_ROOT, WEB_URL

#if WEB_URL.split("/")[3:]:
#    k = "/".join(WEB_URL.split("/")[3:]) + "/"
#else:
k = ""

urlpatterns = patterns('',
     (r'^%s$' % k, mainpage),
     (r'^%spisi/' % k, include('porsuk.pak.urls')),
     (r'^%sadmin/' % k, include('django.contrib.admin.urls')),
     (r"^%smedia/(.*)$" % k, "django.views.static.serve", {"document_root": "%s/media" % DOCUMENT_ROOT, "show_indexes": True}), 
     (r'^i18n/', include('django.conf.urls.i18n')),
)
