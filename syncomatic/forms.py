import os
import shutil, errno

from flask.ext.wtf import Form, BooleanField, PasswordField, Required
from flask.ext.wtf.html5 import EmailField
from flask.ext.wtf.file import FileField

from wtforms.validators import ValidationError, equal_to
from wtforms.fields import HiddenField
from werkzeug import secure_filename

from syncomatic.models import User

class LoginForm(Form):
    email = EmailField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate_email(form, field):
        """The user should exist if one wants to login with him."""
        if not User.query.filter_by(email = field.data).first():
            raise ValidationError("Email is incorrect.")

    def validate_password(form, field):
        """The user should exist if one wants to login with him."""
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if not user.has_password(field.data):
                raise ValidationError("Password is incorrect.")

class RegisterForm(Form):
    email = EmailField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required(),
                             equal_to('confirm_password')])
    confirm_password = PasswordField('confirm_password',
                                     validators = [Required()])

    def validate_email(form, field):
        """Check if the registered user already exists and raise err."""
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Email already registed.")

    def register_user(self):
        """Register a given user."""
        User.add_user(User(self.email.data, self.password.data))

class UploadForm(Form):
    """Form used for uploading files. This form
       is intended only for validation purposes.
    """
    upload = FileField("Upload your image", validators=[Required()])

    def save_file(self, path):
        filename = secure_filename(self.upload.data.filename)
        self.upload.data.save(os.path.join(path, filename))

class CreateFolderForm(Form):
    """Form used for uploading files. This form
       is intended only for validation purposes.
    """
    directory = HiddenField("The new directory", validators=[Required()])

    def create_directory(self, current_path):
        new_dir = os.path.join(current_path, self.directory.data)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

class ShareFileForm(Form):
    """Form used for sharing files. This form
       is intended only for validation purposes.
    """
    path = HiddenField("The share email", validators=[Required()])
    index = HiddenField("The share email", validators=[Required()])
    email = HiddenField("The share email", validators=[Required()])


    def share_directory(self):
        from nose.tools import set_trace; set_trace()
        share_user = User.query.filter_by(email = self.email.data).first()
        if not share_user:
            return

        # TODO the source to share.
        to_share = ''
        # Get home path for the user to share folder with.
        dest = share_user.get_files_path()
        # TODO: uncomment this
        #copyanything(to_share, dest)
