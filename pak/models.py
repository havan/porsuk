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

from django.db import models
from porsuk.settings import WEB_URL, PACKAGE_PREFIX
from django.utils.translation import ugettext as _

class DBDate(models.Model): # Source (Belki Package da)
    # Otomatik olaran nesnenin yaratıldığı zamanı değer olarak alır.
    created = models.DateTimeField(_('DB Creation Date&Time'), auto_now_add=True)
    
    def __unicode__(self):
        return str(self.created)
    
    class Admin:
        pass
    
    class Meta:
        verbose_name = _('Creation Date')
        verbose_name_plural = _('Creation Dates')

class License(models.Model): # Source  
    license = models.CharField(_('License'), max_length=50, unique=True)
    url = models.URLField(_('URL'), blank=True, null=True)

    def __unicode__(self):
        return self.license

    class Admin:
        list_display = ('license', 'url')

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

class Summary(models.Model): # Source  
    lang = models.CharField(_("Language"), max_length=2)
    summary = models.CharField(_('Summary'), max_length=600)

    def __unicode__(self):
        return self.lang.upper() + ' ' + self.summary[:50] + "..."

    class Admin:
        list_display = ('lang', 'summary')

    class Meta:
        verbose_name = _("Summary")
        verbose_name_plural = _("Summaries")

class Description(models.Model): # Source  
    lang = models.CharField(_("Language"), max_length=2)
    desc = models.CharField(_('Description'), max_length=1500)

    def __unicode__(self):
        return self.lang.upper() + ': ' + self.desc[:50] + "..."

    class Admin:
        list_display = ('lang', 'desc')

    class Meta:
        verbose_name = _("Description")
        verbose_name_plural = _("Descriptions")

class Patch(models.Model): # Source 
    name = models.CharField(_('Patch'), max_length=100)
    level = models.IntegerField(_('Level'), null=True)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = _("Patch")
        verbose_name_plural = _("Patches")

class Repo(models.Model): # Source 
    name = models.CharField(_('Name'), max_length=30, unique=True)
    url = models.URLField(_('URL'))
    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ('name', 'url')

    class Meta:
        verbose_name = _("Repository")
        verbose_name_plural = _("Repositories")

class IsA(models.Model): # Source 
    isa = models.CharField(_('IsA'), max_length=50)

    def __unicode__(self):
        return self.isa

    class Admin:
        pass

    class Meta:
        verbose_name = _("Is A")
        verbose_name_plural = _("Is A's")
        
class LocalName(models.Model):
    lang = models.CharField(_("Language"), max_length=2)
    localname = models.CharField(_('Summary'), max_length=200)
    
    def __unicode__(self):
        return self.localname

    class Admin:
        pass

    class Meta:
        verbose_name = _("Local Name")
        verbose_name_plural = _("Local Names")
        
class Component(models.Model): # Source (Package'a da koyulabilir)
    component = models.CharField(_('Component'), max_length=200)
    localname = models.ManyToManyField(LocalName, verbose_name=_('Local Name'), null=True)
    summary = models.ManyToManyField(Summary, verbose_name=_('Summary'), null=True)
    desc = models.ManyToManyField(Description, verbose_name=_('Description'), null=True)
    
    def __unicode__(self):
        return self.component
    
    def get_component_url(self):
        return "/".join(self.component.split("."))

    class Admin:
        pass

    class Meta:
        verbose_name = _("Component")
        verbose_name_plural = _("Components")


class Dependency(models.Model): # Source&Package
    name = models.CharField(_('Dependency'), max_length=80)
    versionFrom = models.CharField(_('Version From'), max_length=35, blank=True, null=True)
    versionTo = models.CharField(_('Version To'), max_length=35, blank=True, null=True)
    version = models.CharField(_('Version'), max_length=35, blank=True, null=True)
    releaseFrom = models.CharField(_('Release From'), max_length=35, blank=True, null=True)
    releaseTo = models.CharField(_('Release To'), max_length=35, blank=True, null=True)
    release = models.CharField(_('Release'), max_length=35, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s/%s/%s" % (WEB_URL, PACKAGE_PREFIX, self.name)

    class Admin:
        list_display = ('name', 'versionFrom')        
    class Meta:
        verbose_name = _("Dependency")
        verbose_name_plural = _("Dependencies")

class Files(models.Model): # Package 
    path = models.CharField(_('Path'), max_length=150)
    fileType = models.CharField(_('fileType'), max_length=50)

    def __unicode__(self):
        return self.fileType + " - " + self.path

    class Admin:
        list_display = ('fileType', 'path')

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

class A_files(models.Model): # Package 
    filename = models.CharField(_('File Name'), max_length=80)
    target = models.CharField(_('Target'), max_length=80, null=True)
    perm = models.IntegerField(_('Permisions'), null=True)
    owner = models.CharField(_('Owner'), max_length=55, null=True)
    group = models.CharField(_('Group'), max_length=55, null=True)

    def __unicode__(self):
        return self.filename

    class Admin:
        list_display = ('filename', 'target', 'owner', 'perm')

    class Meta:
        verbose_name = _('Additional File')
        verbose_name_plural = _('Additional Files')

class IntraFiles(models.Model): # Package
    filename = models.CharField(_('File Name'), max_length=150)
    path = models.CharField(_('Path'), max_length=300)
    type = models.CharField(_('Type'), max_length=80)
    size = models.IntegerField(_('Size'))
    mode = models.IntegerField(_('Mode'))
    hash = models.CharField(_('Hash'), max_length=80)
    
    def __unicode__(self):
        return self.filename
    
    class Admin:
        list_display = ('filename', 'type', 'path')
        fields = (('Genel', {'fields': ('filename', 'type', 'path','size', 'hash', 'mode')}),)

    class Meta:
        verbose_name = _("IntraFile")
        verbose_name_plural = _("IntraFiles")
class Email(models.Model):
    email = models.EmailField(_('Email'))
    
    def __str__(self):
        return self.email
    
    class Admin:
        pass

class Packager(models.Model):
    name = models.CharField(_('Name'), max_length=80)
    email = models.ManyToManyField(Email, verbose_name=_('Email'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Packager')
        verbose_name_plural = _('Packagers')
    
    class Admin:
        list_display = ('name',)

class Update(models.Model): # Source 
    release = models.IntegerField(_('Release'))
    type = models.CharField(_('Type'), max_length=50, null=True)
    date = models.DateField(_('Date'))
    version = models.CharField(_('Version'), max_length=50)
    comment = models.CharField(_('Comment'), max_length=3000)
    packager = models.ForeignKey(Packager, verbose_name=_('Packager'))
    email = models.ManyToManyField(Email, verbose_name=_('Email'))
    
    # Eski paketçi modeli
    #name = models.CharField(_('Name'), max_length=80)
    #email = models.EmailField(_('Email'))

    def __unicode__(self):
        return str(self.release) + "-" + self.version + "-" + self.comment
    
    class Admin:
        list_display = ('release', 'date', 'version', 'packager')

    class Meta:
        verbose_name = _("Update")
        verbose_name_plural = _("Updates")
        get_latest_by = 'date'
        
class Source(models.Model):
    # Repo & Component
    repo = models.ForeignKey(Repo, verbose_name=_('Repository'))
    component = models.ForeignKey(Component, verbose_name=_('Component'))

    # Kaynak bilgileri
    name = models.CharField(_('Name'), max_length=80)
    homepage = models.URLField(_('Homepage'))
    version = models.CharField(_('Version'), max_length=40)

    # Paket bilgileri ForeignKey oluyor. 2 Ocak'08 - 17:48 (İstanbul-Bursa Otobüsü) ;P
    packager = models.ForeignKey(Packager, verbose_name=_('Packager'))
    #packager = models.CharField(_('Packager'), max_length=80)
    #email = models.EmailField(_('Email'))

    license = models.ManyToManyField(License, verbose_name=_("License"))
    isa = models.ManyToManyField(IsA, verbose_name=_('Is A'))
    summary = models.ManyToManyField(Summary, verbose_name=_('Summary'))
    desc = models.ManyToManyField(Description, verbose_name=_('Description'), blank=True, null=True)
    archive_name = models.CharField(_('Name'), max_length=80)
    archive_sha1sum = models.CharField(_('Sha1Sum'), max_length=80)
    archive_type = models.CharField(_('Type'), max_length=10)
    archive_url = models.CharField(_('URL'), max_length=250)
    build_dep = models.ManyToManyField(Dependency, verbose_name=_('Build Dependencies'), related_name='build_dep', null=True, blank=True)
    patch = models.ManyToManyField(Patch, verbose_name=_('Patches'), null=True, blank=True)
    update = models.ManyToManyField(Update, verbose_name=_('Update'))
    packages = models.ManyToManyField("Package", verbose_name=_('Packages'), related_name="packages", null=True, blank=True)
    
    ### Slug ###
    slug = models.SlugField(_('Source Slug'), prepopulate_from=("name",))

    ### İstatistik ###
    last_update = models.DateField(_('Last Update'), blank=True)
    firstReleaseDate = models.DateField(_('First Release Date'), blank=True)
    buildScriptSize = models.IntegerField(_('Build Script Size'), blank=True)
    specScriptSize = models.IntegerField(_('Spec Script Size'), blank=True)
    updateCount = models.IntegerField(_('Update Count'), blank=True)
    patchCount = models.IntegerField(_('Patch Count'), blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "%s/%s/%s/%s" % (WEB_URL, PACKAGE_PREFIX, self.repo.name, self.name)

    def get_spec_url(self):
        return "%s%s/%s" % (self.repo.url, self.component.replace(".", "/"), self.name)

    class Admin:
        list_display = ('name', 'version', 'packager', 'homepage', 'repo', 'component')
        fields = (
            (_('General'), {'fields': ('name', 
                                       'packager', 
                                       'homepage', 
                                       'repo',
                                       'component',
                                       'license',
                                       'isa',
                                       'packages',
                                       'summary',
                                       'desc'),}),
            
            (_('Archive'), {'fields': ('archive_name', 
                                       'archive_url',
                                       'archive_sha1sum',
                                       'archive_type'),
                            'classes': 'collapse'}),

            (_('Other'), {'fields': ('build_dep', 'patch', 'update', 'slug'),
                          'classes': 'collapse'}),

            (_('Statistics'), {'fields': ('last_update',
                                          'firstReleaseDate', 
                                          'buildScriptSize', 
                                          'specScriptSize', 
                                          'updateCount',
                                          'patchCount'),
                               'classes': 'collapse'})
        )
        search_fields = ['name', 'packager']
        ordering=["name"]

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

class Package(models.Model):
    source = models.ForeignKey(Source, verbose_name='Source')
    name = models.CharField(_('Name'), max_length=80)
    slug = models.SlugField(_('Package Slug'), prepopulate_from=("name",))
    runtime_dep = models.ManyToManyField(Dependency, verbose_name=_('Runtime Dependencies'), related_name='runtime_dep', null=True)
    files = models.ManyToManyField(Files, verbose_name=_('Files'))
    a_files = models.ManyToManyField(A_files, verbose_name=_('Additional Files'), null=True)

    ### PiSi-Index'ten gelecek bilgiler ###
    installedSize = models.IntegerField(_('Installed Size'), null=True, blank=True)
    packageSize = models.IntegerField(_('Package Size'), null=True, blank=True)
    packageHash = models.CharField(_('Hash'), max_length=100, null=True, blank=True)
    packageURI = models.CharField(_('URI'), max_length=250, null=True, blank=True)
    #conflicts = mo...
    replaces = models.CharField(_('Replaces'), max_length=100, null=True, blank=True)
    #providesComar = ...
    
    ### Package Files from files.xml ###
    intrafiles = models.ManyToManyField(IntraFiles, verbose_name=_('IntraFiles'), null=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self): # FIXME: 
        return "%s/%s/%s/%s" % (WEB_URL, PACKAGE_PREFIX, self.repo.name, self.name)

    def get_spec_url(self): # FIXME: 
        return "%s%s/%s" % (self.repo.url, self.component.replace(".", "/"), self.name)

    class Admin:
        list_display = ('name', 'source')
        search_fields = ['name', 'runtime_dep']
        ordering=["name"]

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")