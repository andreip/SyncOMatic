import os

from flask import request, send_file
from flask.views import View

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
