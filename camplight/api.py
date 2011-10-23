# -*- coding: utf-8 -*-

"""
Campfire API implementation

The API is described at http://developer.37signals.com/campfire/index
"""

import requests
import simplejson as json

__all__ = ['Request', 'Campfire', 'Room', 'MessageType', 'Sound']


class Request(object):

    _JSON_MEDIA_TYPE = 'application/json'

    def __init__(self, url, token):
        self.url = url
        self._auth = (token, '')

    def _request(self, method, path, data=None):
        headers = None
        if data is not None:
            data = json.dumps(data)
            headers = {'Content-Type': self._JSON_MEDIA_TYPE}

        url = self.url + path + '.json'
        r = requests.request(method, url, data=data, headers=headers,
                             auth=self._auth)
        r.raise_for_status()

        if not self._JSON_MEDIA_TYPE in r.headers['Content-Type']:
            raise TypeError('No JSON in response')

        return json.loads(r.content) if r.content.strip() else None

    def get(self, *args, **kwargs):
        return self._request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request('PUT', *args, **kwargs)


class Campfire(object):

    def __init__(self, request):
        self.request = request

    def account(self):
        return self.request.get('/account')['account']

    def rooms(self):
        return self.request.get('/rooms')['rooms']

    def _room_by_name(self, name):
        return [r for r in self.rooms() if r['name'] == name][0]

    def room(self, room_id):
        try:
            int(room_id)
        except (TypeError, ValueError, OverflowError):
            room_id = self._room_by_name(room_id)['id']
        return Room(self.request, room_id)

    def user(self, user_id=None):
        if user_id is None:
            user_id = 'me'
        return self.request.get('/users/%s' % user_id)['user']

    def presence(self):
        return self.request.get('/presence')['rooms']

    def search(self, term):
        return self.request.get('/search/%s' % term)['messages']


class Room(object):

    def __init__(self, request, room_id):
        self.request = request
        self.room_id = room_id
        self._path = '/room/%s' % self.room_id

    def show(self):
        return self.request.get(self._path)['room']

    def update(self, name=None, topic=None):
        params = {}
        if name is not None:
            params['name'] = name
        if topic is not None:
            params['topic'] = topic
        self.request.put(self._path, data={'room': params})

    def recent(self):
        return self.request.get(self._path + '/recent')['messages']

    def transcript(self):
        return self.request.get(self._path + '/transcript')['messages']

    def uploads(self):
        return self.request.get(self._path + '/uploads')['uploads']

    def join(self):
        self.request.post(self._path + '/join')

    def leave(self):
        self.request.post(self._path + '/leave')

    def lock(self):
        self.request.post(self._path + '/lock')

    def unlock(self):
        self.request.post(self._path + '/unlock')

    def speak(self, message, type_=None):
        params = {'body': message}
        if type_ is not None:
            params['type'] = type_
        data = {'message': params}
        return self.request.post(self._path + '/speak', data=data)['message']


class MessageType(object):
    TEXT = 'TextMessage'
    PASTE = 'PasteMessage'
    SOUND = 'SoundMessage'
    TWEET = 'TweetMessage'


class Sound(object):
    CRICKETS = 'crickets'
    DRAMA = 'drama'
    GREATJOB = 'greatjob'
    LIVE = 'live'
    RIMSHOT = 'rimshot'
    TMYK = 'tmyk'
    TROMBONE = 'trombone'
    VUVUZELA = 'vuvuzela'
    YEAH = 'yeah'