# coding: utf-8

import httplib2
import os
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/calendar'
SECRET_FILE = 'secret.json'
APPLICATION_NAME = 'nicolive reservation to google calendar'


class Google(object):
    def __init__(self, config):
        self.config = config
        self.credentials = self.get_credentials()

    def get_credentials(self):
        pwd = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getcwd())
        credential_path = pwd + '/' + SECRET_FILE
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credential_path, scopes=SCOPES)
        return credentials

    def run(self, event):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        event = service.events().insert(calendarId=self.config.get('calendar_id'), body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    pass
