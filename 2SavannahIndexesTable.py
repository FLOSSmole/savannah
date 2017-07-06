# -*- coding: utf-8 -*-
# Copyright (C) 2004-2017 Megan Squire <msquire@elon.edu>
# License: GPLv3
# 
# Contribution from:
# Caroline Frankel
#
# We're working on this at http://flossmole.org - Come help us build
# an open and accessible repository for data and analyses for free and open
# source projects.
#
# If you use this code or data for preparing an academic paper please
# provide a citation to:
#
# Howison, J., Conklin, M., & Crowston, K. (2006). FLOSSmole:
# A collaborative repository for FLOSS research data and analyses.
# International Journal of Information Technology and Web Engineering, 1(3),
# 17–26.
#
# and
#
# FLOSSmole: a project to provide research access to
# data and analyses of open source projects.
# Available at http://flossmole.org
#
################################################################
# usage:
# python 2SavannahIndexesTable.py <datasource_id> <password>
#
# purpose:
# get the name, url, and html of each savannah project page 
################################################################

import re
import sys
import pymysql
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

datasource_id = '272'

# establish database connection: SYR
try:
    db = pymysql.connect(host='flossdata.syr.edu',
                         user='',
                         passwd='',
                         db='',
                         use_unicode=True,
                         charset="utf8mb4")
    cursor = db.cursor()
except pymysql.Error as err:
    print(err)

selectQuery = 'SELECT project_name FROM sv_projects'

insertQuery = 'INSERT INTO sv_project_indexes (datasource_id, \
                                               project_name, \
                                               indexUrl, \
                                               indexhtml, \
                                               memberhtml, \
                                               date_collected) \
                VALUES(%s, %s, %s, %s, %s, now())'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

try:
    cursor.execute(selectQuery)
    listOfProjects = cursor.fetchall()

    for project in listOfProjects:
        name = project[0]
        print('working on', name)

        indexUrl = 'https://savannah.nongnu.org/projects/' + name
        print(indexUrl)
        req = urllib2.Request(indexUrl, headers=hdr)
        indexhtmlhtml = urllib2.urlopen(req).read()

        memberUrl = 'https://savannah.nongnu.org/project/memberlist.php?group=' + name
        req2 = urllib2.Request(memberUrl, headers=hdr)
        memberhtml = urllib2.urlopen(req2).read()

        try:
            cursor.execute(insertQuery,
                           (datasource_id,
                            name,
                            indexUrl,
                            indexhtmlhtml,
                            memberhtml))
            db.commit()
            print(name, " inserted into indexes table!\n")
        except pymysql.Error as err:
            print(err)
            db.rollback()

except pymysql.Error as err:
    print(err)

except urllib2.HTTPError as herror:
            print(herror)
