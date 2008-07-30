#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

user     = 'porsuk'
dbname   = 'porsuk'
password = 'porsuk'

def usage():
    write = """This is a simple program to create %s database (Postgres)
    
    Usage: python %s [ARG]
    
    installdb\t\t Creates porsuk database with owner porsuk
    uninstalldb\t\t Drops porsuk database
    resetdb\t\t Drops & Creates porsuk database with owner porsuk
    adduser\t\t Creates user porsuk
    removeuser\t\t Drops user porsuk
    sync\t\t Run Django SyncDB
    """ % (dbname, sys.argv[0])
    print write

def checkuser():
    postgres_user = os.system('psql -U postgres -c "select usename from pg_user" |  grep "%s"' % user)
    if postgres_user <> 0 :
        print "You must use first : python %s adduser" % sys.argv[0]
        return False
    else : return True

def installdb():
    print 'Creating %s database.' % dbname
    os.system('createdb %s -U postgres -O %s' % (dbname,user))
    
def syncDB():
    os.chdir('%s/../../' % os.getcwd())
    os.system('python manage.py syncdb')

def uninstalldb():
    print 'Deleting %s database.' % dbname
    os.system('dropdb %s -U postgres' % dbname)

def adduser():
    print 'Creating %s role.' % user
    os.system('psql -U postgres -c "CREATE USER %s ENCRYPTED PASSWORD \'%s\'"' %(user, password))

def removeuser():
    print 'Deleting %s role.' % user
    os.system('dropuser %s -U postgres' % user)

if __name__ == "__main__":
    arg = sys.argv[-1]
    if len(sys.argv) < 2:
        usage()
    elif arg == 'installdb':
        if checkuser() :
            installdb()
            syncDB()
    elif arg == 'uninstalldb':
        uninstalldb()
    elif arg == 'adduser':
        adduser()
    elif arg == 'removeuser':
        removeuser()
    elif arg == "resetdb":
        uninstalldb()
        if checkuser() :
            installdb()
            syncDB()
    elif arg == 'sync':
        syncDB()
    else:
        usage()
