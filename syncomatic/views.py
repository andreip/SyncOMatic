import os

from flask import render_template, redirect, url_for, request, g, send_file
from flask.ext.login import login_user, current_user, logout_user
from flask.views import View
from werkzeug import secure_filename

from syncomatic import app, lm
from syncomatic.decorators import login_required
from syncomatic.forms import LoginForm
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

    def __init__(self, *args, **kwargs):
        super(RootView, self).__init__(*args, **kwargs)
        self.allowed_extensions =\
            set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in self.allowed_extensions

    @login_required
    def dispatch_request(self):
        # If we've got a GET request, just render the template with
        # all the uploaded files by the user.
        if request.method == 'GET':
            files = foos.get_filelist()
            return super(RootView, self).dispatch_request(files=files,
                user=g.user)
        # A file upload was done.
        elif request.method == 'POST':
            file = request.files['file']
            if file:#and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                upload_message = 'File %s was successfully uploaded!' % filename
            else:
                upload_message = 'File not provided or not supported format!'
            # Re-render the index page with upload information regarding the
            # uploaded file through POST.
            files = foos.get_filelist()
            return super(RootView, self).dispatch_request(files=files,
                upload_message=upload_message, user=g.user)


class getFileView(View):
    """
        This view's purpose is to allow a user to download files, thus it does
        not need a template associated with it.
    """
    def dispatch_request(self):
        # Get the file index that is wanted to be downloaded.
        index = request.args.get('index')
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Target the file one wants to download and send it.
        fullpath = app.config['UPLOAD_FOLDER'] + "/" + files[int(index)]
        return send_file(fullpath, as_attachment=True)


class deleteFileView(View):
    """
        This view's purpose is to allow a user to delete a file, thus it does
        not need a template associated with it.
    """
    def dispatch_request(self):
        # Get the file index that is wanted to be deleted.
        index = request.args.get('index')
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Target the file one wants to delete
        fullpath = app.config['UPLOAD_FOLDER'] + "/" + files[int(index)]
        if os.path.isfile(fullpath):
            os.unlink(fullpath)
        # Re-render root page (/)
        return redirect(url_for('index'))


class LoginView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        form = LoginForm()
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


class LogoutView(View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))
