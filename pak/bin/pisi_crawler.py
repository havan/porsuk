#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Ekrem SEREN
# Licensed under the terms of CC Attribution-NonCommercial-ShareAlike 3.0 (CC ByNcSa3)
# See: http://creativecommons.org/licenses/by-nc-sa/3.0/
#
# Created: 09-12-2007 20:23:08

########################################################################
class PisiCrawler:
    """ Lists and downloads pisi packages in a given repository """
    def __init__(self):
        """Constructor"""

    #-------------------------------------------------------------------
    def readRepo(self, repo_url, dest_dir="./"):
        """Reads repo and fetches index files"""
        ### Imports ###
        from pisi.index import Index
        from os import mkdir
        
        ### Check if address got a trailing slash ###
        if repo_url.split("/")[-1]: # If not, add a trailing slash.
            self.repo_url = repo_url + "/"
        else: # Else, use it.
            self.repo_url = repo_url

        ### Check dest_dir ###
        if dest_dir.split("/")[-1]:
            dest_dir = dest_dir + "/"
        
        self.dest_dir = dest_dir + self.repo_url.split("/")[-2]
        self.index_url = self.repo_url + "pisi-index.xml.bz2"
        
        ### Create Pisi-Index instance ###
        self.pi = Index()
        try:
            self.pi.read_uri(self.index_url, self.dest_dir)
        except:
            pass
        self.pi.read((self.dest_dir + "/pisi-index.xml"))
        
    #-------------------------------------------------------------------
    def listPackages(self, fullURI=True):
        """Lists packages for given repo address.
        
        listPackages(fullURI=True)
            
        Set fullURI to False to get just package names.
        """
        ### Iterate over packages ###
        i = 1
        for p in self.pi.packages:
            if fullURI:
                print i, "--", self.repo_url + p.packageURI
            else:
                print i, "--", p.packageURI
            i += 1
            
    #-------------------------------------------------------------------
    def getPackageList(self):
        """Returns a list of package uri's"""
        liste = []
        for p in self.pi.packages:
            p_uri = self.repo_url + p.packageURI
            liste.append(p_uri)
        return liste

    #----------------------------------------------------------------------
    def fetchPackages(self, destination=None):
        """Downloads packages to destination directory """
        from urlgrabber.grabber import URLGrabber
        from urlgrabber.progress import TextMeter
        from os import path, chdir
        
        if destination:
            chdir(destination)
        else:
            chdir(self.dest_dir)
        
        ### URLGrabber objects ###
        t = TextMeter()
        g = URLGrabber(progress_obj=t)
        
        ### Start Iteration over list of packages' URIs ###
        for uri in self.getPackageList():
            pisifile = uri.split("/")[-1]
            if path.exists(pisifile):
                print pisifile, "--- No Update! Skipping..."
                continue
            try:
                g.urlgrab(uri)
            except:
                print "Error while downloading file %s" % pisifile
                break
        print "Finished."
        
    #----------------------------------------------------------------------
    def generatePackageContents(to="cpickle"):
        """Generates lspisi outputs of pisi packages.
        Filetypes; cpickle, pickle, text"""
        pass
        
if __name__=='__main__':
    pass