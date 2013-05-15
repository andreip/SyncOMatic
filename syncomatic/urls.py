# Docs http://flask.pocoo.org/docs/views/ on this structure type.
# Configure View URLs.
from syncomatic import models
from syncomatic import views
from syncomatic import app

from views import RootView, DownloadView, getFileView

app.add_url_rule('/', view_func=RootView.as_view('index',\
    template_name='index.html'))

app.add_url_rule('/download', view_func=DownloadView.as_view('dowload',\
    template_name='download.html'))

app.add_url_rule('/getFile', view_func=getFileView.as_view('getFile'))
