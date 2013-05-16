import os

from flask import request, url_for, render_template, send_file
from flask.views import View
from werkzeug import secure_filename

from syncomatic import app
from syncomatic.forms import LoginForm

class RenderTemplateView(View):
    """
        This views's purpose is to render a given template.
        Extend it at your own will.
    """
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self, *args, **kwargs):
        return render_template(self.template_name, **kwargs)


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

    def dispatch_request(self):
        # If we've got a GET request, just render the template with
        # all the uploaded files by the user.
        if request.method == 'GET':
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return super(RootView, self).dispatch_request(files=files)
        # A file upload was done.
        elif request.method == 'POST':
            file = request.files['file']
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                upload_message = 'File %s was successfully uploaded!' % filename
            else:
                upload_message = 'File not provided or not supported format!'
            # Re-render the index page with upload information regarding the
            # uploaded file through POST.
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return super(RootView, self).dispatch_request(files=files,
                upload_message=upload_message)


class getFileView(View):
    """
        This view's purpose is to allow a user to download files, thus it does
        not need a template associated with it.
    """
    def dispatch_request(self):
        # Get the file index that is wanted to be downloaded.
        index = request.args.get('index')
        from syncomatic import app
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # Target the file one wants to download and send it.
        fullpath = app.config['UPLOAD_FOLDER'] + "/" + files[int(index)]
        return send_file(fullpath, as_attachment=True)


class LoginView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        form = LoginForm()
        return super(LoginView, self).dispatch_request(title='Sign In',
                                                       form=form)

