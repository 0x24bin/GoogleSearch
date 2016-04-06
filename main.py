#!/usr/bin/python

import requests
import json
import urllib
import sys
import re
import os
from urlparse import urljoin
from bs4 import BeautifulSoup
import MySQLdb

def GSearch(q):
    query = urllib.urlencode({'q': q})
    
    sites = []
    try:
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query

        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            sites.append(h['url'])

        url1 = url + '&start=4'
        search_response = urllib.urlopen(url1)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            sites.append(h['url'])

        url1 = url + '&start=8'
        search_response = urllib.urlopen(url1)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            sites.append(h['url'])

        url1 = url + '&start=12'
        search_response = urllib.urlopen(url1)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            sites.append(h['url'])

        url1 = url + '&start=16'
        search_response = urllib.urlopen(url1)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results['responseData']
        hits = data['results']
        for h in hits:
            sites.append(h['url'])
    except TypeError, ConnectionError:
        pass
    return sites

# def CrawlPage(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     print '' + soup.title.name
#     print url
#     print
#     print soup.body.get_text()
#     links = set()
#     for link in soup.find_all('a', href=True):
#         links.add(link['href'])
#     print
#     print links
#     print
    # print len(links)

def CrawlPage(url):
    try:
        request = requests.get(url)
        html = html = " ".join(line.strip() for line in request.content.split("\n"))
        soup = BeautifulSoup(html, 'html.parser')
        for elem in soup.find_all(['script', 'style', 'iframe']):
            elem.extract()
        t = soup.title
        if t == None:
            t = "No Title"
        else:
            t = t.string
        title = t.strip().encode('utf-8')
        b = soup.body
        if b == None:
            b = "No text"
        else:
            b = soup.body.get_text()
        body = b.encode('utf-8')
        flag = any(x in body.lower() for x in ['seed', 'leech'])
        links_set = set()
        for link in soup.find_all('a', href=True):
            if 'http' in link['href']:
                links_set.add(link['href'].split('#')[0].encode('utf-8'))
            else:
                links_set.add(urljoin(url, link['href']).split('#')[0].encode('utf-8'))
        links = []
        for link in links_set:
            links.append(link)
        return title, body, json.dumps(links), str(flag)
    except requests.exceptions.ConnectionError:
        return "", "", "", ""


class Database:

    host = '127.0.0.1'
    user = 'root'
    password = 'password' 
    db = 'development_db'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()
        
    def getTermID(self, r):
        q = "SELECT id FROM `Terms` WHERE terms = '{}';".format(r)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        data =  cursor.fetchone()
        return False if data == None else data['id']

    def getURLID(self, u):
        q = "SELECT id FROM `URL` WHERE url = '{}';".format(u)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(q)
        data =  cursor.fetchone()
        return False if data == None else data['id']

    def insertTerm(self, t):
        try:
            query = "INSERT INTO development_db.Terms(terms) VALUES ('{}');".format(t)
            self.cursor.execute(query)
            self.connection.commit()
            return self.getTermID(t)
        except:
            print "error insertTerm"
            self.connection.rollback()
            return False
    
    def insertURL(self, u, t, b, f, l):
        try:
            title = MySQLdb.escape_string(t)
            body = MySQLdb.escape_string(b)
            url = MySQLdb.escape_string(u)
            links = MySQLdb.escape_string(l)
            query = "INSERT INTO development_db.URL(url, title, body_text, flag, links) VALUES ('{}', '{}', '{}', '{}', '{}');".format(url, title, body, f, links)
            self.cursor.execute(query)
            self.connection.commit()
            return self.getURLID(u)
        except MySQLdb.Error as err:
            print "insertURL: Something went wrong: {}".format(err)
            print u
            self.connection.rollback()
            return False

    def linkExists(self, tID, uID):
        query = "SELECT count(*) FROM development_db.TermsURL WHERE termID = {} and urlID = {};".format(tID, uID)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data =  cursor.fetchone()
        return data['count(*)'] != 0


    def insertLink(self, tID, uID):
        # check if link exists
        if self.linkExists(tID, uID):
            return
        try:
            query = "INSERT INTO development_db.TermsURL(termID, urlID) VALUES ({}, {})".format(tID, uID)
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except:
            print "error insertLink"
            self.connection.rollback()
            return False

    def search(self, search):
        v = MySQLdb.escape_string(search)
        query = "SELECT url, title, body_text FROM  `development_db`.`URL` WHERE body_text REGEXP '{}';".format(v)
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        data =  cursor.fetchall()
        return data
    
    def __del__(self):
        self.connection.close()

def printMenu(msg):
    print msg
    print '------------'
    print '1. Search'
    print '2. Display'
    print '9. Exit'
    print '------------'
    var = raw_input("Please make a selection: ")
    var.strip()
    if var == '1':
        search()
    elif var == '2':
        display()
    elif var == '9':
        print "Bye!"
        sys.exit()
    else:
        _ = os.system("clear")
        printMenu('wong chooice, try again!')

def search():
    var = raw_input('Search: ')
    if len(var) > 0:
        termID = db.getTermID(var)
        if not termID:
            termID = db.insertTerm(var)
        
        sites = GSearch(var)
        for site in sites:
            # check if site exists in DB
            urlID = db.getURLID(site)
            if urlID:
                # link the url to the term
                db.insertLink(termID, urlID)
            else:
                t, b, l, f = CrawlPage(site)
                urlID =  db.insertURL(site, t, b, f, l)
                if urlID:
                    db.insertLink(termID, urlID)
    else: 
        _ = os.system("clear")
        printMenu("Found just what you searched for, nothing")

def display():
    var = raw_input("What would you like to display? ")
    if len(var) > 0:
        data = db.search(var)
        print len(data), "result(s)"
        for d in data:
            print
            print d['title']
            print d['url']
            body = " ".join(d['body_text'].split())
            print (body[:30] + '...') if len(body) > 30 else body
        print
        print len(data), "result(s) for", var 
            
    else:
        _ = os.system("clear")
        printMenu("Nothing to diaplay")


if __name__ == '__main__':
    db = Database()
    _ = os.system("clear")
    printMenu('')
