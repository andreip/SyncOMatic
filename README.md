SyncOMatic
==========

#SyncOMatic

##How to run:

* install flask, follow [docs guide](http://flask.pocoo.org/docs/installation/#installation)
* install all needed packets from `requirements.txt` file, all using `pip install $name`
* `$ ./run.py` opens server listening on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* login credentials: the user is **admin@example.com**, for *password* enter anything not blank, doesn't matter


##What it can do (in progress):

* upload a file using the file chooser, and store it in **project/files/**
* download a file (to local) that was uploaded
* login and logout with a user in the app, it doesn't take into account the password for now and
  no registrations possible for now, just hardcoded account created in the database
  ** database is in `syncomatic/static/syncomatic.db`
