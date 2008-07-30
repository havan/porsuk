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

from django.shortcuts import get_object_or_404, render_to_response, Http404
from porsuk.settings import PACKAGES_PER_PAGE
from porsuk.pak.models import *
from django.views.generic.list_detail import object_list
from time import time
from django.db.models import Q

from django.utils.translation import ugettext as _

def mainpage(request): 
    return render_to_response('main.html')

def packages(request, orderby): 
    queryset = Package.objects.all().order_by(orderby)
    return object_list(request,
                       queryset,
                       template_object_name='packages', 
                       template_name='pak/packages.html',
                       paginate_by=PACKAGES_PER_PAGE,
                   )

def package(request, id):
    queryset = Package.objects.get(pk=id)
    return render_to_response('pak/package.html', {'package': queryset,})

def sources(request,orderby):
    queryset = Source.objects.all().order_by(orderby)
    return object_list(request,
                       queryset,
                       template_object_name='sources', 
                       template_name='pak/sources.html',
                       paginate_by=PACKAGES_PER_PAGE,
                   )
def source(request, id):
    queryset = Source.objects.get(pk=id)
    return render_to_response('pak/source.html', {'source': queryset,})

def repositories(request):
    queryset = Source.objects.get(pk=id)
    return render_to_response('pak/repositories.html', {'source': queryset,})

def repository(request, repo, type):
    if type == "packages":
        queryset = Package.objects.filter(source__repo__name=repo).order_by('name')
        return object_list(request,
                           queryset,
                           template_object_name='packages', 
                           template_name='pak/packages.html',
                           paginate_by=PACKAGES_PER_PAGE,
                       )
    if type == "sources":
        queryset = Source.objects.filter(repo__name=repo).order_by('name')
        return object_list(request,
                           queryset,
                           template_object_name='sources', 
                           template_name='pak/repository.html',
                           paginate_by=PACKAGES_PER_PAGE,
                       )

def packagers(request, orderby):
    queryset = Packager.objects.order_by(orderby)
    return object_list(request,
                       queryset,
                       template_object_name='packagers', 
                       template_name='pak/packagers.html',
                   )    

def packager_info(request, name, type):
    if type == "sources":
        pkgr = Packager.objects.get(name=name)
        queryset = Source.objects.filter(packager=pkgr)
        return object_list(request,
                           queryset,
                           template_object_name='sources', 
                           template_name='pak/packager_sources.html',
                           paginate_by=PACKAGES_PER_PAGE,
                       )
    elif type == "updates":
        pkgr = Packager.objects.get(name=name)
        queryset = Update.objects.filter(packager=pkgr)
        return object_list(request,
                           queryset,
                           template_object_name='updates', 
                           template_name='pak/packager_updates.html',
                           paginate_by=PACKAGES_PER_PAGE,
                       )
    else:
        return Http404

def packager(request, name):
    pkgr = Packager.objects.get(name=name)
    last_updates = pkgr.update_set.order_by('-date')[:5]
    last_sources = pkgr.update_set.filter(release=1)[:5]
    return render_to_response('pak/packager.html', {'packager': pkgr,
                                                    'last_updates': last_updates,
                                                    'last_sources': last_sources,
                                                } )


def updates(request, orderby="-date", type=None):
    if type:
        queryset = Update.objects.all().order_by(orderby).filter(type=type)
    else:
        queryset = Update.objects.all().order_by(orderby)
    return object_list(request,
                       queryset,
                       template_object_name='updates', 
                       template_name='pak/updates.html',
                       paginate_by=PACKAGES_PER_PAGE,
                   )

def update(request, id):
    queryset = Update.objects.get(pk=id)
    return render_to_response('pak/update.html', {'update': queryset,} )


def search(request, pattern, orderby='name'):
    starttime = time()
    #queryset = Source.objects.filter(name__icontains=pattern).order_by(orderby)
    queryset = Source.objects.filter(Q(name__icontains=pattern) | Q(summary__summary__icontains=pattern) | Q(desc__desc__icontains=pattern)).order_by(orderby)
    #print queryset
    took = (time()-starttime)
    return object_list(request,
                   queryset,
                   template_object_name='sources', 
                   template_name='pak/search.html',
                   paginate_by=PACKAGES_PER_PAGE,
                   extra_context = {'took': took,}
               )
    

"""
def packager_packages(request, pkger):
    queryset=Source.objects.filter(packager__icontains=pkger)
    return object_list(request,
                       queryset,
                       template_object_name='source', 
                       template_name='pak/packager_paks.html',
                       paginate_by=PACKAGES_PER_PAGE,
                   )
def source_detail(request, repo, pak):
    queryset=Source.objects.get(name=pak, repo__name=repo)
    return render_to_response('pak/source_detail.html', {'source': queryset,} )"""
