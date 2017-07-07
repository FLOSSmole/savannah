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
# python 4SavannahDevelopersProjectsTable.py <datasource_id> <password>
#
# purpose:
# Gets what developers worked on what project
################################################################

import re
import sys
import pymysql
from bs4 import BeautifulSoup

datasource_id = '272'


def run():
    try:
        cursor.execute(insertQuery,
                       (datasource_id,
                        dev_loginname,
                        name))
        db.commit()
        print(name, " updated in developer projects3dldf table!\n")
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

selectQuery = 'SELECT project_name, memberhtml FROM sv_project_indexes' # LIMIT 2'

insertQuery = 'INSERT INTO sv_developer_projects (datasource_id, \
                                                  dev_loginname, \
                                                  project_name, \
                                                  date_collected) \
                VALUES (%s, %s, %s, now())'
try:
    cursor.execute(selectQuery)
    listOfProjects = cursor.fetchall()

    for project in listOfProjects:
        name = project[0]
        html = project[1]
        print('\nworking on', name)
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        userRegex = '<a href=\"/users/(.*?)\"'
        
        td = soup.find_all('td')
        for t in td:
            userList = re.findall(userRegex, str(t))
            if userList:
                for user in userList:
                    dev_loginname = user
                    print(dev_loginname)
                    run()

except pymysql.Error as err:
    print(err)
