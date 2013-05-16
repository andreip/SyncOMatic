from flask.ext.sqlalchemy import SQLAlchemy

from syncomatic import app
db = SQLAlchemy(app)
# Create tables when running models.
db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30), unique=True)

    def __init__(self, email, password):
        self.email = email
        # TODO(andreip): hack, save file in plaintext.
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email
