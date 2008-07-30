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

### Imports ###
import os, sys
from time import time
from pisi.specfile import SpecFile
from pisi.component import Component as PisiComponent # Component modeli ile çakışıyor

### PythonPath ve Django Settings'i ekle ###
sys.path.append('%s/../../../' % os.getcwd())
os.environ["DJANGO_SETTINGS_MODULE"] = 'porsuk.settings'

### Import models from Porsuk ###
from porsuk.pak.models import *
from django.db import transaction

### SVN Depoları ###
svn_repositories = (
    ('devel', 'http://svn.pardus.org.tr/pardus/devel/'),
    ('pardus-2007', 'http://svn.pardus.org.tr/pardus/2007/'),
    ('pardus-2008', 'http://svn.pardus.org.tr/pardus/2008/'),
    ('contrib-devel', 'http://svn.pardus.org.tr/contrib/devel/'),
    ('contrib-2007', 'http://svn.pardus.org.tr/contrib/2007/'),
    ('contrib-2008', 'http://svn.pardus.org.tr/contrib/2008/'),
    #('playground', 'http://svn.pardus.org.tr/pardus/playground/'), # Playground sonda dursun
)

### Derlenen depolar ###
package_repositories = (
    ('pardus-2007', 'http://paketler.pardus.org.tr/pardus-2007/'),
    ('pardus-2008', 'http://paketler.pardus.org.tr/pardus-2008/'),
    ('contrib-2007', 'http://paketler.pardus.org.tr/contrib-2007/'),
    ('contrib-2008', 'http://paketler.pardus.org.tr/contrib-2008/'),
    ('pardus-2007-test', 'http://paketler.pardus.org.tr/pardus-2007-test/'),
    ('pardus-2008-test', 'http://paketler.pardus.org.tr/pardus-2008-test/'),
)

### Veritabanına girme sırasında atlanacak paketleri belirtir ###
package_blacklist = []

### SVN CheckOut klasörü tanımla ###
home = os.environ.get('HOME')
svndir       = 'porsuk-svn'
expsvndir = 'porsuk-svn/exported'

### Usage Help ###
def usage():
    print """\nPorsuk Database populater.
Usage: python %s [ARG]

checkout\t\t Checks out svn repositories.
run\t\t\t Starts filling database.
corun\t\t\t First Checks out repos then starts to fill database.
""" % sys.argv[0]

# FIXME: İşlemden önce svn klasörlerinde güncelleme çalıştır
#        ve export et. -- FIXED 12-12-2007 19:08:32
def checkout():
    """svn_repositories'de tanımlı depoları günceller ve export eder."""
    checkout_starttime = time()
    for reponame, repourl in svn_repositories:
        npath = os.path.join(home, svndir, reponame)
        epath = os.path.join(home, expsvndir, reponame)
        if not os.path.isdir(npath):
            print 'Repository : %s bulunamadı, indiriliyor...' % reponame
            try:
                os.system('svn co %s %s' % (repourl, npath))
            except:
                print 'Repository : %s indirilirken hata oluştu...' % reponame
        else:
            print 'Repository : %s güncelleniyor...' % reponame
            try:
                os.system('svn up %s' % npath)
            except:
                print 'Repository : %s güncellenirken hata oluştu...' % reponame

        print 'Repository : %s export ediliyor...' % reponame
        try:
            if not os.path.exists(epath):
                os.mkdir(epath)
            os.system('rm -rf %s' %epath)
            os.system('svn export %s %s' % (npath, epath))
        except:
            print 'Repository : %s export edilemedi' % reponame

    global checkout_totaltime
    checkout_totaltime = (time() - checkout_starttime)
    print "SVN CHECKOUT %.2f sn sürdü." % checkout_totaltime

### Betik satır sayısı al ###
def getFileSize(src):
    """Verilen dosyanın satır sayısını döndürür"""
    src_file = open(src)
    len = src_file.readlines().__len__()
    src_file.close()
    return len

### Transaction'ı kendin kontrol et ###
@transaction.commit_manually # Transaction kullanımı veritabanı performansını büyük ölçüde arttırdı.
def fillDB():
    """Veritabanını svn klasörlerinden aldığı bilgiler ile doldurur."""
    ### Toplam süreyi ölç ###
    startTime=time()

    ### Save DB Creation Date ###
    db_creation_date = DBDate()
    db_creation_date.save()

    sayac = 1 # Paket sayısı

    for repo_name, repo_url in svn_repositories:
        for root, dirs, files in os.walk(os.path.join(home, expsvndir, repo_name)):
            for file in files:
                if file == 'pspec.xml':
                    spec = SpecFile(os.path.join(root, file))

                    ### Paket BlackList'te ise atla ###
                    if spec.source.name in package_blacklist:
                        print "%s BlackList'te. Atlanıyor..." % spec.source.name
                        sayac += 1
                        continue

                    ### FIXME: Read from database and retrieve saved package objects,
                    ### FIXME: there should be no need to erase all database everytime.

                    ### Bilgi yaz ###
                    print "\033[01;33m%s\033[0m - %s - (Paket \033[01;33m%d\033[0m)" % (spec.source.name, repo_name, sayac),

                    ### Bir döngü süresi zamanı al ###
                    packStartTime = time()

                    ### Repo ###
                    r, r_created = Repo.objects.get_or_create(name=repo_name, url=repo_url)
                    if r_created:
                        r.save()

                    ### Depoda aynı kaynak varsa (isim ve repo'ya göre) bu paketi atla ###
                    if not repo_name == "playground":
                        try:
                            s = Source.objects.get(name=spec.source.name, repo=r)
                            print "Kaynak mevcut. Atlanıyor..."
                            sayac += 1
                            continue
                        except:
                            pass

                    ### Source nesnesini yarat ###
                    s = Source()
                    s.repo = r

                    ### Source Verileri ###
                    s.name=spec.source.name
                    s.homepage = spec.source.homepage
                    s.version = spec.getSourceVersion()

                    ### Packager nesnesini yarat veya al ###
                    pkgr, pkgr_created = Packager.objects.get_or_create(name=spec.source.packager.name)
                    email, email_created = Email.objects.get_or_create(email=spec.source.packager.email)
                    if email_created:
                        email.save()
                    pkgr.email.add(email)
                    pkgr.save()

                    s.packager = pkgr

                    # Packager nesnesinden önceki durum
                    #s.packager = spec.source.packager.name
                    #s.email = spec.source.packager.email

                    s.archive_name = spec.source.archive.name
                    s.archive_sha1sum = spec.source.archive.sha1sum
                    s.archive_type = spec.source.archive.type
                    s.archive_url = spec.source.archive.uri

                    ### Slug ###
                    s.slug = spec.source.name

                    ### İstatistikler ###
                    s.last_update = spec.history[0].date
                    s.firstReleaseDate = spec.history[-1].date
                    s.buildScriptSize = getFileSize(os.path.join(root, 'actions.py'))
                    s.specScriptSize = getFileSize(os.path.join(root, file))
                    s.updateCount = spec.history.__len__()
                    s.patchCount = spec.source.patches.__len__()

                    ### Component nesnesi ###
                    try: # Component.xml'den almayı dene
                        comp_file = PisiComponent(os.path.join(root, '../component.xml'))
                        component, comp_created = Component.objects.get_or_create(component=comp_file.name)
                        if comp_created:
                            ### Sadece nesne yaratıldığında M2M alanları girmek component.xml bulamayıp
                            ### klasör isminden çıkardığı zaman Component nesnesini diğer bilgilerden
                            ### yoksun bıracak. Buna temiz bir çözüm bulmalı ya da Playground'un en son
                            ### işlendiğinden emin olmalı.
                            ###
                            ### Component nesnesi için Summary döngüsü ###
                            for localname_lang in comp_file.localName.keys():
                                localname = LocalName(lang=localname_lang,
                                                      localname=comp_file.localName[localname_lang])
                                localname.save()
                                component.localname.add(localname)

                            ### Component nesnesi için Summary döngüsü ###
                            for comp_summary_lang in comp_file.summary.keys():
                                comp_summary = Summary(lang=comp_summary_lang,
                                                       summary=comp_file.summary[comp_summary_lang])
                                comp_summary.save()
                                component.summary.add(comp_summary)
                            ### Component nesnesi için Summary döngüsü ###
                            for comp_desc_lang in comp_file.description.keys():
                                comp_desc = Description(lang=comp_desc_lang,
                                                        desc=comp_file.description[comp_desc_lang])
                                comp_desc.save()
                                component.desc.add(comp_desc)
                            ### Döngüler bitince Component nesnesini kaydet ###
                            component.save()
                        ### Source'a bağla ###
                        s.component = component

                    except: # Component.xml yoksa klasör isminden çıkar
                        print "Could not find component.xml, trying to retrieve component from directories"
                        dir_comp = root[:root.rfind('/')].replace(os.path.join(home, expsvndir, repo_name) + '/','').replace("/",".")
                        component, comp_created = Component.objects.get_or_create(component=dir_comp)
                        if comp_created:
                            component.save()
                        s.component = component

                    ### Source kaydet ###
                    s.save()

                    ### License ###
                    for l in spec.source.license:
                        li, li_created = License.objects.get_or_create(license=l)
                        if li_created:
                            li.save()
                        s.license.add(li)

                    ### IsA ###
                    for i in spec.source.isA:
                        isa, isa_created = IsA.objects.get_or_create(isa=i)
                        if isa_created:
                            isa.save()
                        s.isa.add(isa)

                    ### Summary ###
                    for su in spec.source.summary.keys():
                        sum, sum_created = Summary.objects.get_or_create(summary=spec.source.summary[su])
                        if sum_created:
                            sum.lang = su
                            sum.save()
                        s.summary.add(sum)

                    ### Description ###
                    if not spec.source.description.keys():
                        bos, bos_created = Description.objects.get_or_create(desc=" ")
                        if bos_created:
                            bos.lang = " "
                            bos.save()
                        s.desc.add(bos)

                    for de in spec.source.description.keys():
                        des, des_created = Description.objects.get_or_create(desc=spec.source.description[de])
                        if des_created:
                            des.lang = de
                            des.save()
                        s.desc.add(des)

                    ### Build Dependencies ###
                    for bu in spec.source.buildDependencies:
                        bd, bd_created = Dependency.objects.get_or_create(name=bu.package,
                                                                          versionFrom=bu.versionFrom,
                                                                          versionTo=bu.versionTo,
                                                                          version=bu.version,
                                                                          releaseFrom=bu.releaseFrom,
                                                                          releaseTo=bu.releaseTo,
                                                                          release=bu.release,
                                                                          )
                        if bd_created:
                            bd.save()
                        s.build_dep.add(bd)


                    ### Patches ###
                    for pec in spec.source.patches:
                        patch = Patch(name=pec.filename, level=pec.level)
                        patch.save()
                        s.patch.add(patch)

                    ### Updates ###
                    for h in spec.history:
                        updater, updater_created = Packager.objects.get_or_create(name=h.name)
                        u_email, u_email_created = Email.objects.get_or_create(email=h.email)
                        if u_email_created:
                            u_email.save()
                        updater.email.add(u_email)
                        updater.save()

                        history = Update(release=h.release,
                                         type=h.type,
                                         date=h.date,
                                         version=h.version,
                                         comment=h.comment,
                                         packager=updater,
                                         #name=h.name,
                                         #email=h.email,
                                     )
                        history.save()
                        history.email.add(u_email)
                        s.update.add(history)

                    ######### PACKAGE #########
                    ### Package nesneleri için döngü ###
                    for package in spec.packages:
                        ### Package nesnesini yarat ###
                        p = Package(name=package.name, source=s, slug=package.name)
                        #p, p_created = Package.objects.get_or_create(name=package.name, source=s)
                        #if not p_created:
                        #    print "%s paketi mevcut. Atlanıyor..." % p.name
                        p.save()

                        ### Package'ı Source'a bağla
                        s.packages.add(p)

                        ### RuntimeDeps ##
                        for run_dep in package.packageDependencies:
                            runtime_dep, rundep_created = Dependency.objects.get_or_create(name=run_dep.package,
                                                                                           versionFrom=run_dep.versionFrom,
                                                                                           versionTo=run_dep.versionTo,
                                                                                           version=run_dep.version,
                                                                                           releaseFrom=run_dep.releaseFrom,
                                                                                           releaseTo=run_dep.releaseTo,
                                                                                           release=run_dep.release,
                                                                                       )
                            if rundep_created:
                                runtime_dep.save()
                            p.runtime_dep.add(runtime_dep)

                        ### Files ###
                        for fi in package.files:
                            pfile, file_created = Files.objects.get_or_create(path=fi.path, fileType=fi.fileType)
                            if file_created:
                                pfile.save()
                            p.files.add(pfile)

                        ### Additional Files ###
                        for add_file in package.additionalFiles:
                            af = A_files(filename=add_file.filename,
                                         target=add_file.target,
                                         perm=add_file.permission,
                                         owner=add_file.owner,
                                         group=add_file.group,
                                     )
                            af.save()
                            p.a_files.add(af)

                    ### PRINTS ###
                    print "\033[01;33m%.3f s\033[0m" %(time() - packStartTime),
                    print "- %d s" % (time() - startTime)
                    sayac += 1
    ### Veritabanına commit et ###
    print "Döngüler bitti, veritabanına commit ediliyor..."
    trans_time = time()
    transaction.commit()
    print "Veriler girildi. (%f sn)" % (time() - trans_time)
    print "Bitti. Toplam işlem süresi %.2f dakika." % ((time() - startTime)/60)

################################

if __name__ == "__main__":
    arg = sys.argv[-1]
    if len(sys.argv) < 2:
        usage()
    elif arg == "checkout":
        checkout()
    elif arg == "run":
        fillDB()
    elif arg == "corun":
        checkout()
        fillDB()
        print "(%.2f dk SVN CO & EXPORT süresi hariç)" % (checkout_totaltime/60)
    else:
        usage()
