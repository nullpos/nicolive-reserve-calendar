# coding: utf-8

import urllib2
import cookielib
import json
import re
import datetime
from bs4 import BeautifulSoup as BS

LOGIN_URL = 'https://secure.nicovideo.jp/secure/login'


class Live(object):
    def __init__(self, config):
        self.config = config
        self.opener = self.create_opener()

    def create_opener(self):
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        opener.open(LOGIN_URL, "mail=%s&password=%s" %
            (self.config.get('mail'), self.config.get('password')))
        return opener

    def get(self, url):
        html = self.opener.open(url).read()
        soup = BS(html, 'html.parser')
        live_info = self.parse_live_page(soup)
        return live_info

    def parse_live_page(self, soup):
        live_info = {}

        title_el = soup.find(class_='gate_title')
        # alive
        if title_el:
            title = title_el.span.get_text()
            main_el = soup.find(class_='textbox')

            kaijo_text = main_el.find(class_='hmf').get_text()
            date = re.search(u'(\d{4}\/\d{2}\/\d{2})', kaijo_text).group(1)
            time = re.search(u'開演\:(\d{2}\:\d{2})', kaijo_text).group(1)

            detail_el = main_el.find(id='jsFollowingAdMain')
            # div element exist if not official live
            if detail_el.div:
                detail_el.div.extract()
            detail = []
            for s in detail_el.strings:
                detail.append(s)
            detail.pop(0)
            for i in range(0, len(detail)):
                detail[i] = re.sub(r'^\n', '', detail[i])
            detail[0] = re.sub(r'^\t{4}', '', detail[0])
            detail[-1] = re.sub(r'\n\t$', '', detail[-1])
            detail = ('\n'.join(detail))

            start = re.sub('/', '-', date) + 'T' + time + ':00'
            dt = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=1)
            end = dt.isoformat()

            live_info['summary'] = title
            live_info['description'] = detail
            live_info['start'] = {
                'dateTime': start + '+09:00'
            }
            live_info['end'] = {
                    'dateTime': end + '+09:00'
            }

        return live_info


if __name__ == '__main__':
    pass
