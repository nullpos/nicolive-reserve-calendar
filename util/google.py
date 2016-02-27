# coding: utf-8

import httplib2
import os
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.readonly']
SECRET_FILE = 'secret.json'
APPLICATION_NAME = 'nicolive reservation to google calendar'


class Google(object):
    def __init__(self, config):
        self.config = config
        self.service = self.get_service()

    def get_service(self):
        pwd = os.path.join(os.path.dirname(os.path.dirname(__file__)), os.getcwd())
        credential_path = pwd + '/' + SECRET_FILE
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credential_path, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def insert(self, event):
        event = self.service.events().insert(
                calendarId=self.config.get('calendar_id'), body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    def search(self, live_info, url):
        event_list = self.service.events().list(
                calendarId=self.config.get('calendar_id'),
                q=live_info.get('summary'),
                singleEvents=True).execute()
        return event_list.get('items')[0].get('id')

    def delete(self, live_info, url):
        event_id = self.search(live_info, url)
        self.service.events().delete(calendarId=self.config.get('calendar_id'),
                eventId=event_id).execute()
        print('Event deleted.')

    def update(self, live_info, url):
        event_id = self.search(live_info, url)
        event = self.service.events().update(calendarId=self.config.get('calendar_id'),
                eventId=event_id).execute()
        print('Event updated: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    pass
