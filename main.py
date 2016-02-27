# coding: utf-8

import os
import re
import sys
import ConfigParser
from util.live import Live
from util.google import Google

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config'
CONFIG_SAMPLE_FILE = CONFIG_PATH + '.sample'
LIVE_BASE_URL = 'http://live.nicovideo.jp/watch/'

class Main(object):
    def __init__(self):
        config_path = CONFIG_PATH
        if not os.path.exists(config_path):
            config_path = CONFIG_SAMPLE_FILE
        self.config = self.get_config(config_path)

    def get_config(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        nico = 'niconico'
        google = 'google'

        nicomail = config.get(nico, 'mail')
        password = config.get(nico, 'password')
        calendar_id = config.get(google, 'calendar_id')

        dictionary = {
            nico: {
                'mail': nicomail,
                'password': password
            },
            google: {
                'calendar_id': calendar_id
            }
        }

        return dictionary

    def run(self, url, method):
        live = Live(main.config.get('niconico'))
        live_info = live.get(url)
        google = Google(main.config.get('google'))

        if method == 'insert':
            google.insert(live_info)
        elif method == 'update':
            google.update(live_info, url)
        elif method == 'delete':
            google.delete(live_info, url)
        elif method == 'search':
            google.search(live_info, url)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "invalid arguments"

    method = sys.argv[1]
    if re.match('lv', sys.argv[2]):
        url = LIVE_BASE_URL + sys.argv[2]
    else:
        url = sys.argv[2]
    main = Main()
    main.run(url, method)
