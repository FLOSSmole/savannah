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
# python 5SavannahDevelopersTable.py <datasource_id> <password>
#
# purpose:
# get information on the developers
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
                        dev_loginname,
                        real_name,
                        description,
                        infohtml,
                        skillshtml,
                        member_since,
                        developer_id))
        db.commit()
        print(name, " updated in developers table!\n")
    except pymysql.Error as err:
        print(err)
        db.rollback()


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

selectQuery = 'SELECT project_name, memberhtml FROM sv_project_indexes'

insertQuery = 'INSERT IGNORE INTO sv_developers (datasource_id, \
                                                 dev_loginname, \
                                                 real_name, \
                                                 description, \
                                                 infohtml, \
                                                 skillshtml, \
                                                 member_since, \
                                                 developer_id, \
                                                 date_collected) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())'

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
        html = project[1]
        print('\nworking on', name)

        soup = BeautifulSoup(html, 'html.parser')
        userRegex = '<a href=\"/users/(.*?)\">(.*?) &lt'

        td = soup.find_all('td')

        for t in td:
            userList = re.findall(userRegex, str(t))
            if userList:
                for user in userList:
                    dev_loginname = user[0]
                    print('dev_loginname: ', dev_loginname)

                    real_name = user[1]
                    print('real_name: ', real_name)

                    userUrl = 'https://savannah.gnu.org/users/' + dev_loginname
                    req = urllib2.Request(userUrl, headers=hdr)
                    infohtml = urllib2.urlopen(req).read()

                    soup2 = BeautifulSoup(infohtml, 'html.parser')
                    idRegex = '<td>Id: </td>\s*<td><strong>#(.*?)</strong></td>'
                    idFinder = re.findall(idRegex, str(soup2))
                    if idFinder:
                        developer_id = idFinder[0]
                        print('developer_id: ', developer_id)

                    memberSinceRegex = '<td>Site Member Since:\s*</td>\s*<td>\s*<strong>(.*?)</strong>'
                    memberSinceFinder = re.findall(memberSinceRegex, str(soup2))
                    if memberSinceFinder:
                        memberSince = memberSinceFinder[0]
                        memberSinceList = memberSince.split(' ')
                        month = month_converter(memberSinceList[2])
                        year = memberSinceList[3]
                        day = memberSinceList[1]
                        time = memberSinceList[4]
                        member_since = '{}-{}-{} {}'.format(year, month, day, time)
                        print('member_since: ', member_since)

                    skillsUrl = 'https://savannah.nongnu.org/people/resume.php?user_id=' + developer_id

                    try:
                        req2 = urllib2.Request(skillsUrl, headers=hdr)
                        skillshtml = urllib2.urlopen(req2).read()
                        soup3 = BeautifulSoup(skillshtml, 'html.parser')

                        p = soup3.find_all('p')
                        descriptionLine = p[1]
                        description = ''
                        for desc in descriptionLine:
                            description = description + str(desc)
                        print('description: ', description)

                    except:
                        skillshtml = None
                        description = None

                    run()

except pymysql.Error as err:
    print(err)

except urllib2.HTTPError as herror:
            print(herror)
