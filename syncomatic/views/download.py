import os

from flask import render_template, make_response
from syncomatic.views.render_template import RenderTemplateView

class DownloadView(RenderTemplateView):
    def __init__(self, *args, **kwargs):
        super(DownloadView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        from syncomatic import app
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('download.html', files = files)
