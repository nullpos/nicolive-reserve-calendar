# coding: utf-8

import os
import ConfigParser
from util.live import Live
from util.google import Google

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + '/config'
CONFIG_SAMPLE_FILE = CONFIG_PATH + '.sample'

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

    def run(url):
        pass



if __name__ == '__main__':
    url = ''
    main = Main()
    live = Live(main.config.get('niconico'))
    info = live.get(url)
    print info
    google = Google(main.config.get('google'))
    google.run(info)
