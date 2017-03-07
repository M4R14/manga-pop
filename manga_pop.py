#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import lxml.html
import urllib
import urllib.request
import json
import time
import datetime
import smtplib
import sys

from subprocess import call
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from urllib.request import Request, urlopen
from email.mime.multipart import MIMEMultipart

def writeLog(text):
    pass

def sendmail_(Subject, img, txt_message):
    username = 'vachirawit.mark@gmail.com'
    password = 'Mark00009999'

    me = 'vachirawit.mark@gmail.com'
    you = 'vachirawit.mark@gmail.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = Subject
    msg['From'] = me
    msg['To'] = you

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = ("""\
    <html>
      <head></head>
      <body>
        <h1>Manga-POP</h1> by <a href="https://web.facebook.com/vachirawit.laolod">Mark.Vachi</a>
        <hr>
        <table>
          <tr><h2>%s</h2></tr>
          <tr>
            <td>%s</td>
            <td>
                <ul>%s</ul>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """ % (Subject, img, txt_message))

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com:587')

    s.starttls()
    s.login(username,password)
    s.sendmail(me, you, msg.as_string())
    s.quit()

def job():
    with open('manga.json') as json_data:
        manga = json.load(json_data)

    with open('log.json') as json_data:
        log = json.load(json_data)

    with open('log.json') as json_data:
        data_log = json.load(json_data)

    timeStamp = ''
    for mangName in manga['manga']:
        req = Request(manga['manga'][mangName], headers={'User-Agent': 'Mozilla/5.0'})
        mysite = urlopen(req).read()
        soup_mysite = BeautifulSoup(mysite, 'lxml')
        description = soup_mysite.find("ul", {"class": "lst"}) # meta tag description

        txt_ntfy = ''
        txt_message = ''

        count = 0
        for li in description:
            # text = description.find('a')
            text = li.find('a')
            point_macth = 0;
            for log_li in log:
                if text['href'] == log_li['link']:
                    point_macth = point_macth + 1;
                    break

            if point_macth == 0:
                count = count + 1
                rawtime = time.time()
                timeStamp = datetime.datetime.fromtimestamp(rawtime).strftime('%Y-%m-%d %H:%M:%S')
                title = text['title']
                data = {
                    "title" : title,
                    "link" : text['href'],
                    "timestamp": timeStamp
                }
                txt_ntfy = txt_ntfy + title + '\n'
                txt_message = txt_message + '<li><a href="'+ text['href'] +'?all">' + title +'</a></li>'
                data_log.append(data)

        # txt_message = txt_message + '</ul>'
        # print(mangName)
        # print(manga['manga'][mangName])
        if count == 0:
            print('[null] ' + mangName )
        else:
            img = soup_mysite.find("img", {"class": "cvr"})
            tag_img = "<img width='180' src='"+ img['src'] +"'><br>"
            title = mangName + " have " + str(count) + " Update."
            sendmail_(title, tag_img , txt_message)
            print("-----------------------------------------------")
            print(title)
            print("-----------------------------------------------")
            print(txt_ntfy)
            print("-----------------------------------------------\n")

            call(['ntfy','--title', title ,'send', 'By Mark.Vachi' ])
            # print(data_log)
            with open('log.json', 'w') as f:
                json.dump(data_log, f)
        # pass

while 1:
    # eval("print('Hello')")
    job()
    rawtime = time.time()
    timeStamp = datetime.datetime.fromtimestamp(rawtime).strftime('%Y-%m-%d %H:%M:%S')
    print("----- "+ timeStamp +" ------")
    # sys.stdout.write("----- "+ str(timeStamp) +" ------")
    time.sleep(60*10)
