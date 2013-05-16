from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = TextField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
