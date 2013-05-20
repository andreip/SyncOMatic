import os

from flask import render_template, redirect, url_for, request, g, send_file
from flask.ext.login import login_user, current_user, logout_user
from flask.views import View
from werkzeug import secure_filename

from syncomatic import app, lm
from syncomatic.decorators import login_required
from syncomatic.forms import LoginForm, RegisterForm
from syncomatic.models import User
from syncomatic import foos

class RenderTemplateView(View):
    """
        This views's purpose is to render a given template.
        Extend it at your own will.
    """
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self, *args, **kwargs):
        return render_template(self.template_name, **kwargs)


@lm.user_loader
def load_user(id):
    """Has the purpose of telling flask-login what to use
       to load a user from database. Hence the decorator.
    """
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


class RootView(RenderTemplateView):
    """
        This view manages the index page, and displays all the
        uploaded files by a user and also it provides a form
        for uploading new files.
    """
    methods = ['GET', 'POST']

    @login_required
    def dispatch_request(self):
        # Get the user directory.
        user_dir = g.user.get_files_path()

        # If we've got a GET request, just render the template with
        # all the uploaded files by the user.
        if request.method == 'GET':
            files = foos.get_filelist(user_dir)
            return super(RootView, self).dispatch_request(files=files,
                user=g.user)
        # A file upload was done.
        elif request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(user_dir, filename))
                upload_message = 'File %s was successfully uploaded!' % filename
            else:
                upload_message = 'File not provided or not supported format!'
            files = foos.get_filelist(user_dir)
            # Re-render the index page with upload information regarding the
            # uploaded file through POST.
            return super(RootView, self).dispatch_request(files=files,
                upload_message=upload_message, user=g.user)


class getFileView(View):
    """
        This view's purpose is to allow a user to download files, thus it does
        not need a template associated with it.
    """
    def get_filepath_by_index(self, index):
        # Get the user directory.
        user_dir = g.user.get_files_path()
        # Get the file index that is wanted to be downloaded.
        files = os.listdir(user_dir)
        # Target the file one wants to download and send it.
        fullpath = os.path.join(user_dir, files[int(index)])
        return fullpath

    def dispatch_request(self):
        index = request.args.get('index')
        return send_file(self.get_filepath_by_index(index), as_attachment=True)


class deleteFileView(getFileView):
    """
        This view's purpose is to allow a user to delete a file, thus it does
        not need a template associated with it.
    """
    def dispatch_request(self):
        index = request.args.get('index')
        # Target the file one wants to delete
        fullpath = self.get_filepath_by_index(index)
        if os.path.isfile(fullpath):
            os.unlink(fullpath)
        # Re-render root page (/)
        return redirect(url_for('index'))


class LoginView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        # User has logged in successfully before.
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            # If user exists in our DB, log him in.
            if user:
                login_user(user, remember = form.remember_me.data)
                return redirect(url_for('index'))
            return redirect(url_for('login'))
        return super(LoginView, self).dispatch_request(title='Sign In',
                                                       form=form)

class RegisterView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(RegisterView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        # User has logged in successfully before.
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))
        form = RegisterForm()
        if form.validate_on_submit():
            form.register_user()
            # Now redirect the user to login so he may login.
            return redirect(url_for('login'))
        return super(RegisterView, self).dispatch_request(title='Register',
                                                          form=form)


class LogoutView(View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))
