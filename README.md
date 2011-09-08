Camplight
=========

Camplight is a standalone command-line client for Campfire written in Python.

The Campfire API is documented here: http://developer.37signals.com/campfire/index


Usage
-----

    $ export CAMPFIRE_URL=https://your-subdomain.campfirenow.com
    $ export CAMPFIRE_TOKEN=your_auth_token

    $ camplight rooms
    $ camplight presence
    $ camplight user me

    $ CAMPFIRE_ROOM=12345 camplight recent

    $ CAMPFIRE_ROOM="Develop" camplight join
    $ CAMPFIRE_ROOM="Develop" camplight speak "You should check out Camplight"


License
-------

See LICENSE file.


Contact
-------

* Web: <https://github.com/misfire/Camplight>
* Mail: <mathias.lafeldt@gmail.com>
