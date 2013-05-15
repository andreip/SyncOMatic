from flask import Flask

app = Flask(__name__)

# The folder where files will be uploaded.
import os

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# The folder where files will be uploaded.
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_FOLDER, 'files')

# The database URI that should be used for the connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' %\
    os.path.join(PROJECT_FOLDER, 'static', 'syncomatic.db')

# Create some directories if they don't exist already.
# We need some directories to be created so that our app
# can create the database inside it or to check the uploaded files,
# and git does not allow us to commit empty directories.
DIRS_IN_PROJECT = ['static', 'files']
for d in DIRS_IN_PROJECT:
    # Compute the directory path appending the name to the
    # current path of the project, example
    # /abs/path/application/static/
    d = os.path.join(PROJECT_FOLDER, d)
    if not os.path.exists(d):
        os.makedirs(d)

import urls
