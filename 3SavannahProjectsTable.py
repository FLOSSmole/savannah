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
# python 3SavannahProjectsTable.py <datasource_id> <password>
#
# purpose:
# get the name, url, and html of each savannah project page 
################################################################

import re
import sys
import pymysql
from bs4 import BeautifulSoup

datasource_id = '272'


def run():
    try:
        cursor.execute(updateQuery,
                       (description,                # 1
                        id_num,                     # 2
                        project_dev_count,          # 3
                        project_group_type,         # 4
                        number_of_mailing_lists,    # 5
                        bugs_open,                  # 6
                        bugs_total,                 # 7
                        techsupp_open,              # 8
                        techsupp_total,             # 9
                        looking_for_number,         # 10
                        taskmgr_open,               # 11
                        taskmgr_total,              # 12
                        patchmgr_open,              # 13
                        patchmgr_total,             # 14
                        licenses,                   # 15
                        development_status,         # 16
                        registration_date,          # 17
                        datasource_id,
                        name))
        db.commit()
        print(name, " updated in projects table!\n")
    except pymysql.Error as err:
        print(err)
        db.rollback()


def regexMaker(regex):
    regexFinder = re.findall(regex, str(soup))
    if regexFinder:
        word = regexFinder[0]
        return word


def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1


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

selectQuery = 'SELECT project_name, indexhtml FROM sv_project_indexes'  # WHERE project_name = "freeride" LIMIT 1'

updateQuery = 'UPDATE sv_projects SET description = %s, \
                                      id_num = %s, \
                                      project_dev_count = %s, \
                                      project_group_type = %s, \
                                      number_of_mailing_lists = %s, \
                                      bugs_open = %s, \
                                      bugs_total = %s, \
                                      techsupp_open = %s, \
                                      techsupp_total = %s, \
                                      looking_for_number = %s, \
                                      taskmgr_open = %s, \
                                      taskmgr_total = %s, \
                                      patchmgr_open = %s, \
                                      patchmgr_total = %s, \
                                      license = %s, \
                                      development_status = %s, \
                                      registration_date = %s, \
                                      date_collected = now() \
            WHERE datasource_id = %s AND project_name = %s'

try:
    cursor.execute(selectQuery)
    listOfProjects = cursor.fetchall()

    for project in listOfProjects:
        name = project[0]
        html = project[1]
        print('\nworking on', name)

        soup = BeautifulSoup(html, 'html.parser')

        desc = soup.find('div', {'class':'indexcenter'})
        p = desc.find_all('p')
        description = ''
        for line in p:
            try:    
                for line.contents in line:
                    if isinstance(line.contents, str):
                        description = description + ' ' + line.contents
                    else:
                        for l in line.contents:
                            description = description + l

            except:
                try:
                    for l in line:
                        if isinstance(l, str):
                            description = description + l
                        else:
                            for section in l:
                                for s in section:
                                    if len(s) > 1:
                                        description = description + s
                except:
                    for li in line:
                        if isinstance(li, str) is False:
                            for i in li:
                                if isinstance(i, str) is False:
                                    for i2 in i:
                                        if isinstance(i2, str) is False:
                                            for i3 in i2:
                                                if isinstance(i3, str) is False:
                                                    for i4 in i3:
                                                        if isinstance(i4, str) is False:
                                                            for i5 in i4:
                                                                if isinstance(i5, str) is True:
                                                                    description = description + i5
                                                        else:
                                                            description = description + i4
                                                else:
                                                    description = description + i3
                                        else:
                                            description = description + i2
                                else:
                                    description = description + i
                        else:
                            description = description + li
                        # description = description + str(li)

        print('1: ', description)
        
        id_num = regexMaker('group_id=(.*?)\">')
        print('2: ', id_num)

        span = soup.find_all('span')
        for s in span:
            if 'active member' in str(s):
                strong = s.find('strong')
                project_dev_count = strong.contents[0]
                print('3: ', project_dev_count)

        project_group_type = regexMaker('Group Type: <strong>(.*?)</strong>')
        print('4: ', project_group_type)

        number_of_mailing_lists = regexMaker('<strong>(.*?)</strong> public mailing-list')
        print('5: ', number_of_mailing_lists)

        bugs = regexMaker('Bug Tracker</a> \(<strong>(.*?)</strong> open items, <strong>(.*?)</strong> total')
        if bugs:
            bugs_open = bugs[0]
            print('6: ', bugs_open)

            bugs_total = bugs[1]
            print('7: ', bugs_total)

        tech = regexMaker('Tech Support Manager</a> \(<strong>(.*?)</strong> open items, <strong>(.*?)</strong> total')
        if tech:
            techsupp_open = tech[0]
            print('8: ', techsupp_open)

            techsupp_total = tech[1]
            print('9: ', techsupp_total)

        looking_for_number = regexMaker('looking for people</a> \(<strong>(.*?)</strong>')
        print('10: ', looking_for_number)

        taskmgr = regexMaker('Task Manager</a> \(<strong>(.*?)</strong> open items, <strong>(.*?)</strong> total')
        if taskmgr:
            taskmgr_open = taskmgr[0]
            print('11: ', taskmgr_open)

            taskmgr_total = taskmgr[1]
            print('12: ', taskmgr_total)

        patchmgr = regexMaker('Patch Manager</a> \(<strong>(.*?)</strong> open items, <strong>(.*?)</strong> total')
        if patchmgr:
            patchmgr_open = patchmgr[0]
            print('13: ', patchmgr_open)

            patchmgr_total = patchmgr[1]
            print('14: ', patchmgr_total)
        
        try:
            licenseLine = description.split('License:')[1]
            licenses = licenseLine.split('Development')[0].strip()
            print('15: ', licenses)
        except:
            licenses = None

        try:
            development_status = licenseLine.split('Development')[1].strip()
            print('16: ', development_status)
        except:
            development_status = None

        registrationLine = description.split('Date:')[1]
        registrationLine2 = registrationLine.split('License:')[0].strip()
        regLine = registrationLine2.split(' ')
        month = month_converter(regLine[2])
        registration_date = '{}-{}-{} {}'.format(regLine[3], month, regLine[1], regLine[4])
        print('17: ', registration_date)

        run()
except pymysql.Error as err:
    print(err)
