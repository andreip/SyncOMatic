import os

from flask.ext.sqlalchemy import SQLAlchemy
from syncomatic import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, email, password):
        self.email = email
        # TODO(andreip): hack, save file in plaintext.
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)


def init_db():
    """Delete old database, init a new one and populate it.
       We do this to sync changes on the models, when runnig
       run.py.

       Order is important. This has to be called only after the User
       model has been defined.
    """
    if os.path.exists(app.config['SQLALCHEMY_DATABASE_URI_PATH']):
        os.unlink(app.config['SQLALCHEMY_DATABASE_URI_PATH'])
    db.create_all()
    db.session.add(User('admin@example.com', 'password'))
    db.session.commit()

init_db()
