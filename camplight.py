"""
Campfire API implementation in Python

The API is described at http://developer.37signals.com/campfire/index
"""

__author__ = 'Mathias Lafeldt <mathias.lafeldt@gmail.com>'
__data__ = ['Campfire', 'CampfireRoom']

import urllib2
import simplejson as json

class Campfire(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        passwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwd_manager.add_password(None, uri=self.url, user=self.token, passwd='X')
        auth_handler = urllib2.HTTPBasicAuthHandler(passwd_manager)
        self.url_opener = urllib2.build_opener(auth_handler)

    def get(self, path):
        response = self.url_opener.open(self.url + path).read()
        return json.loads(response) if response.startswith('{') else {}

    def post(self, path, data={}):
        request = urllib2.Request(self.url + path, json.dumps(data))
        request.add_header('Content-Type', 'application/json')
        response = self.url_opener.open(request).read()
        return json.loads(response) if response.startswith('{') else {}

    def put(self, path, data={}):
        request = urllib2.Request(self.url + path, json.dumps(data))
        request.add_header('Content-Type', 'application/json')
        request.get_method = lambda: 'PUT'
        response = self.url_opener.open(request).read()
        return json.loads(response) if response.startswith('{') else {}

    def rooms(self):
        return self.get('/rooms.json')['rooms']

    def room(self, id):
        try:
            int(id)
        except:
            id = [r['id'] for r in self.rooms() if r['name'] == id][0]
        return CampfireRoom(self, id)

    def user(self, id='me'):
        return self.get('/users/%s.json' % id)['user']

    def presence(self):
        return self.get('/presence.json')['rooms']

    def search(self, term):
        return self.get('/search/%s.json' % term)['messages']


class CampfireRoom(object):
    def __init__(self, campfire, room_id):
        self.campfire = campfire
        self.room_id = room_id

    def get(self, path, **kwargs):
        return self.campfire.get('/room/%s%s' % (self.room_id, path), **kwargs)

    def post(self, path, **kwargs):
        return self.campfire.post('/room/%s%s' % (self.room_id, path), **kwargs)

    def put(self, path, **kwargs):
        return self.campfire.put('/room/%s%s' % (self.room_id, path), **kwargs)

    def show(self):
        return self.get('.json')['room']

    def set_name(self, name):
        self.put('.json', data={'room': {'name': name}})

    def set_topic(self, topic):
        self.put('.json', data={'room': {'topic': topic}})

    def recent(self):
        return self.get('/recent.json')['messages']

    def transcript(self):
        return self.get('/transcript.json')['messages']

    def uploads(self):
        return self.get('/uploads.json')['uploads']

    def join(self):
        self.post('/join.json')

    def leave(self):
        self.post('/leave.json')

    def lock(self):
        self.post('/lock.json')

    def unlock(self):
        self.post('/unlock.json')

    def speak(self, message, type='TextMessage'):
        data = {'message': {'body': message, 'type': type}}
        return self.post('/speak.json', data=data)['message']

    def paste(self, message):
        return self.speak(message, 'PasteMessage')

    def play(self, sound):
        return self.speak(sound, 'SoundMessage')
