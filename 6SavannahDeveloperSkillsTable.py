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
# python 6SavannahDeveloperSkillsTable.py <datasource_id> <password>
#
# purpose:
# get skills of the developers
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
                        skill,
                        level,
                        experience))
        db.commit()
        print(dev_loginname, " updated in dev skills table!\n")
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

selectQuery = 'SELECT dev_loginname, skillshtml FROM sv_developers WHERE skillshtml iS NOT NULL'

insertQuery = 'INSERT INTO sv_dev_skills (datasource_id, \
                                          dev_loginname, \
                                          skill, \
                                          level, \
                                          experience, \
                                          date_collected) \
                VALUES (%s, %s, %s, %s, %s, now())'

try:
    cursor.execute(selectQuery)
    listOfProjects = cursor.fetchall()

    for project in listOfProjects:
        dev_loginname = project[0]
        html = project[1]
        print('\nworking on', dev_loginname)

        soup = BeautifulSoup(html, 'html.parser')

        tr = soup.find_all('tr')
        for t in tr:
            td = t.find_all('td')
            if td:
                if isinstance(td[0].contents[0], str):
                    skill = td[0].contents[0]
                    print('skill: ', skill)
                else:
                    line = td[0].contents[0]
                    regex = '<p class=\"warn\">\((.*?)\)'
                    regexFinder = re.findall(regex, str(line))
                    if regexFinder:
                        skill = regexFinder[0]
                        print('skill: ', skill)

                try:
                    level = td[1].contents[0]
                    print('level: ', level)
                except:
                    level = None

                try:
                    experience = td[2].contents[0]
                    print('experience: ', experience)
                except:
                    experience = None

                run()

except pymysql.Error as err:
    print(err)
