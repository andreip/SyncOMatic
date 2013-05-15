import os

from flask import request, url_for, render_template
from werkzeug import secure_filename

from syncomatic.views.render_template import RenderTemplateView
from syncomatic import app

class RootView(RenderTemplateView):
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
