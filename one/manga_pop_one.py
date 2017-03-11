# -*- coding: utf-8 -*-
import fire
import json
import urllib
import urllib.request
import sys
import os
import time

from progress.bar import Bar
from subprocess import call
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from urllib.request import Request, urlopen

class manga_pop(object):
  _manga_file_name = 'manga1.json'
  _log_file_mane = 'log1.json'
  _full_log = []

  def __init__(self):
    # call(['chcp','65001'])
    self._updateLog()

    os.system('chcp 65001')

    with open(self._log_file_mane) as json_data:
        self._full_log = json.load(json_data)
    pass

  def _updateLog(self, type='manga'):
      with open(self._log_file_mane) as json_data:
          data_log = json.load(json_data)

      manga = self._getManga()
      newManga = []
      if type == 'manga':
          for site in manga:
              for cartoon in manga[site]:
                  point_macth = 0;
                  for manga_log in data_log:
                      if manga_log['name'] == cartoon:
                          point_macth = point_macth + 1;
                          break
                      pass

                  if point_macth == 0:
                    #   print(cartoon)
                      data_log.append({"name":cartoon, "chapter":[]})
                      pass
              pass

          with open(self._log_file_mane, 'w') as f:
               json.dump(data_log, f)
          pass
    #   print(data_log)
      pass

  def _getMangaLog(self, manga_name='Kingdom'):
      for manga in self._full_log:
          if manga['name'] == manga_name:
              return manga
              break
      pass

  def _getLog(self, manga_name='Kingdom'):
      with open(self._log_file_mane) as json_data:
          log = json.load(json_data)

      for manga in log:
          if manga['name'] == manga_name:
              return manga
              break
      return 'null'

  def _getManga(self):
      with open(self._manga_file_name) as json_data:
          manga = json.load(json_data)
      return manga
      pass

  def list(self):
    manga = self._getManga()

    for site in manga:
        print('-------------------\n', site, '\n-------------------');
        number = 1;
        for cartoon in manga[site]:
            print(str(number)+').', cartoon, '_____________________', manga[site][cartoon] );
            number = number+1;
            pass
    # return 2 * number

  def _getMangaFormLink(self, site='', link=''):
      onSite = []
      if site == 'niceoppai':
          req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
          mysite = urlopen(req).read()
          soup_mysite = BeautifulSoup(mysite, 'lxml')
          description = soup_mysite.find("ul", {"class": "lst"}) # meta tag description

          for li in description:
              tag_a = li.find('a')
              data = {
                  "title" : tag_a['title'],
                  "link" : tag_a['href'],
              }
              onSite.append(data)
          return onSite

  def update(self):
    #   self._updateLog()
      bar = Bar('Processing', max=100)
      manga = self._getManga()
      poin_update = 0
      list_update = [];

      for site in manga:
        for cartoon in manga[site]:
            bar.next()
            index = 0
            for log in self._full_log:
                if log['name'] == cartoon:
                    link = manga[site][cartoon]
                    # print(cartoon, '[', link,']');
                    onSite = self._getMangaFormLink(site, link)
                    if len(log['chapter']) == 0:
                        poin_update = poin_update + 1
                        self._full_log[index]['chapter'] = onSite
                        # print('--- ', log['chapter'][0]['title']);
                    pass

                    if len(log['chapter']) > 0:
                        for chapter_onSite in onSite:
                            point_macth = 0
                            for chapter in log['chapter']:
                                if chapter == chapter_onSite:
                                    point_macth = point_macth + 1;
                                    break
                                    pass

                            if point_macth == 0:
                                # print(chapter_onSite)
                                poin_update = poin_update + 1
                                data = {"name":cartoon, "link":link, "chapter":chapter_onSite}
                                list_update.insert(0, data)
                                self._full_log[index]['chapter'].insert(0, chapter_onSite)
                                pass
                            pass
                    pass
                # if poin_update > 0:
                    # call(['ntfy','--title', cartoon ,'send', 'By Mark.Vachi' ])
                index = index + 1
                # time.sleep(0.01)
            os.system('cls')
            bar.finish()

      if poin_update > 0:
          with open(self._log_file_mane, 'w') as f:
               json.dump(self._full_log, f)
          old = ''
          for list_manga in list_update:
            #   print(list_manga)
              if not old == list_manga['name']:
                  old = list_manga['name']
                  print(list_manga['name'], len(list_manga['chapter']), 'update.')
                  print('---------------------------------------------------')
                  pass
              print('  +',list_manga['chapter']['title'], '>>',list_manga['chapter']['link'])
              pass
          print('---------------------------------------------------')
          pass
      if poin_update == 0:
          print(" 0 Update.");
          pass
      pass

if __name__ == '__main__':
  fire.Fire(manga_pop)
