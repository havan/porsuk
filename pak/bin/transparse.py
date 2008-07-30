#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel

langs = ['tr','en','fr','nl','pl','it','es','de']

class Translation:
    def __init__(self,xmlfile):
        self.tfile = xmlfile
        self.SourceSummary = {}
        self.PackageSummary = {}
        self.SourceDescription = {}
        self.PackageDescription = {}
        self.SourceName = ''
        self.PackageName = ''

    def parsexmldata(self):
        xmldata = piksemel.parse(self.tfile)
        for sroottag in xmldata.tags('Source'):#Source blok bilgilerini al
            self.SourceName = sroottag.getTagData('Name')
            try:
                for stag in sroottag.tags('Summary'):
                    slang = stag.getAttribute('xml:lang')
                    scontent = stag.firstChild().data()
                    self.SourceSummary[slang] = scontent
            except:
                print "Source(Summary) Yok"
            try:
                for dtag in sroottag.tags('Description'):
                    dlang = dtag.getAttribute('xml:lang')
                    dcontent = dtag.firstChild().data()
                    self.SourceDescription[dlang] = dcontent
            except:
                print "Source(Description) yok"

        for droottag in xmldata.tags('Package'):#Package blok bilgilerini al
            self.PackageName = droottag.getTagData('Name')
            try:
                for stag in droottag.tags('Summary'):
                    slang = stag.getAttribute('xml:lang')
                    scontent = stag.firstChild().data()
                    self.PackageSummary[slang] = scontent
            except:
                print "Package(Summary) Yok"
            try:
                for dtag in droottag.tags('Description'):
                    dlang = dtag.getAttribute('xml:lang')
                    dcontent = dtag.firstChild().data()
                    self.PackageDescription[dlang] = dcontent
            except:
                print "Package(Description) yok"

t = Translation('translations.xml')
t.parsexmldata()
print t.SourceSummary , t.SourceDescription
print t.PackageSummary , t.PackageDescription

