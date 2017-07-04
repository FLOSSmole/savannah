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
# python 1SavannahWebScraper.py <datasource_id> <password>
#
# purpose:
# grab a list of the projects on Launchpad
# get the project name, project long name, and gnu or non of each savannah project 
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


def run():
    try:
        cursor.execute(insertQuery,
                       (datasource_id,
                        project_name,
                        project_long_name,
                        gnu_or_non))
        db.commit()
        print(project_name, " inserted into projects table!\n")
    except pymysql.Error as err:
        print(err)
        db.rollback()

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

insertQuery = 'INSERT INTO sv_projects (datasource_id, \
                                         project_name, \
                                         project_long_name, \
                                         gnu_or_non, \
                                         date_collected) \
            VALUES(%s, %s, %s, %s, now())'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

try:
    url = 'https://savannah.gnu.org/search/?type_of_search=soft&words=%2A&offset=0&max_rows=5000#results'
    req = urllib2.Request(url, headers=hdr)
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html, 'html.parser')
    tr = soup.find_all('tr')
    i = 1
    # gets project name and project long name
    regex1 = '<tr class=\"(.*?)\"><td><a href=\"\.\./projects/(.*?)\">(.*?)</a></td>'

    # gets whether the project is gnu or non-gnu
    regex2 = '</td><td>(.*?)</td></tr>'

    for t in tr:
        infoLineFinder = re.findall(regex1, str(t))
        print(i)
        i = i+1

        if infoLineFinder:
            project_name = infoLineFinder[0][1]
            print('project name: ', project_name)

            project_long_name = infoLineFinder[0][2]
            print('project long name: ', project_long_name)

        gnuFinder = re.findall(regex2, str(t))
        if gnuFinder:
            if 'portions' not in gnuFinder[0]:
                if 'translation teams' not in gnuFinder[0]:
                    if 'non-GNU' in str(gnuFinder):
                        gnu_or_non = 'nongnu'
                    else:
                        gnu_or_non = 'gnu'

            print('gnu or non: ', gnu_or_non)

        run()

except pymysql.Error as err:
    print(err)
