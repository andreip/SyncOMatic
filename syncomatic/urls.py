# Docs http://flask.pocoo.org/docs/views/ on this structure type.
# Configure View URLs.
from syncomatic import views
from syncomatic import app

app.add_url_rule('/', view_func=views.RootView.as_view('index',\
    template_name='index.html'))

app.add_url_rule('/getFile', view_func=views.getFileView.as_view('getFile'))

app.add_url_rule('/login', view_func=views.LoginView.as_view('login',\
    template_name='login.html'))
