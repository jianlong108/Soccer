#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# from urllib2 import Request
import requests
import sqlite3
import os




def download(url):
    # print("downloading", url)
    try:
        html = requests.urlopen(url).read()
    except requests.URLError as e:
        print("download error")
        html = None
    return html


def getHtmlListWithLabel(html, label,attrs={}):

    soup = BeautifulSoup(html, "html.parser")

    trList = []
    if attrs != {}:
        tr_ni = soup.find_all(label,attrs=attrs)
    else:
        tr_ni = soup.find_all(label)

    trList.extend(tr_ni)
    return trList

def getSoup(html):

    soup = BeautifulSoup(html, "html.parser")

    return soup

def filterList(list, label):
    tempList = []
    tempList.extend(list)
    for ele in list:
        value = str(ele).find(label)
        if value < 0:
            tempList.remove(ele)

    return tempList

location = os.path.expanduser('~/Desktop/Soccer.db')
def create_database():
    global conn
    global c

    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect(location)
    c = conn.cursor()

    # sql = 'create table if not exists ' + 'Soccer' + \
    #       '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,league varchar(20),soccer VARCHAR(5),gameurl VARCHAR (30),otodds VARCHAR(5) ,' \
    #       'orignalpan VARCHAR(5),ododds VARCHAR(5),ntodds VARCHAR(5) ,nowpan VARCHAR(5),ndodds VARCHAR(5))'
    # c.execute(sql)

    sql0 = 'create table if not exists ' + 'Games' + \
          '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,'\
            'soccerID INTEGER,league varchar(20),time VARCHAR(15),result INTEGER,' \
          'homeLevel INTEGER,home VARCHAR(20),homeSoccer INTEGER,'\
            'friendLevel INTEGER,friend VARCHAR(20) ,friendSoccer INTEGER)'

    c.execute(sql0)

    sql1 = 'create table if not exists ' + 'CompanyHandicap' + \
          '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,gameid INTEGER,company VARCHAR(10),otodds REAL ,' \
          'orignalpan REAL,ododds REAL,ntodds REAL ,nowpan REAL,ndodds REAL)'
    c.execute(sql1)

    sql2 = 'create table if not exists ' + 'CompanyODD' + \
           '(soccer_ID INTEGER PRIMARY KEY AUTOINCREMENT,gameid INTEGER,company VARCHAR(10),' \
           'ori_winODD REAL ,ori_drawODD REAL,ori_loseODD REAL,'\
            'winODD REAL ,drawODD REAL,loseODD REAL)'
    c.execute(sql2)

    conn.commit()
    c.close()
    conn.close()


def insert_record(params):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    # sql = 'insert into ' + table_name + '(num, league,soccer,gameurl,otodds,orignalpan,ododds,ntodds,nowpan,ndodds) values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(game.leauge,game.soccer,game.url,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)

    c.execute("INSERT INTO Soccer VALUES (NULL ,?,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()
def insert_Game(params):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    # sql = 'insert into ' + table_name + '(num, league,soccer,gameurl,otodds,orignalpan,ododds,ntodds,nowpan,ndodds) values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(game.leauge,game.soccer,game.url,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)

    c.execute("INSERT INTO Games VALUES (NULL ,?,?,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()



def insert_Handi(params):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    # sql = 'insert into ' + table_name + '(num, league,soccer,gameurl,otodds,orignalpan,ododds,ntodds,nowpan,ndodds) values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(game.leauge,game.soccer,game.url,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)

    c.execute("INSERT INTO CompanyHandicap VALUES (NULL ,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

def insert_ODD(params):
    conn = sqlite3.connect(location)
    c = conn.cursor()
    # sql = 'insert into ' + table_name + '(num, league,soccer,gameurl,otodds,orignalpan,ododds,ntodds,nowpan,ndodds) values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(game.leauge,game.soccer,game.url,company.orignal_top,company.orignal,company.orignal_bottom,company.now_top,company.now,company.now_bottom)

    c.execute("INSERT INTO CompanyODD VALUES (NULL ,?,?,?,?,?,?,?,?)", params)
    # c.execute(sql)
    conn.commit()
    c.close()
    conn.close()