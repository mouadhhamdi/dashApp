from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
import dash_auth
from werkzeug.serving import run_simple
import dash_html_components as html
VALID_USERNAME_PASSWORD_PAIRS = [
    ['FinController', 'FinController']
]



server = flask.Flask(__name__)
dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/' )
dash_app2 = Dash(__name__, server=server, url_base_pathname='/reports/')
dash_app2.layout = html.Div([html.H1('Hi there, I am app2 for reports')])

auth = dash_auth.BasicAuth(
    dash_app1,
    VALID_USERNAME_PASSWORD_PAIRS
)


@server.route('/')
def hello():
    return "hne"


@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/dash1')


@server.route('/reports')
def render_reports():
    return flask.redirect('/dash2')

app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server,
})

run_simple('0.0.0.0', port=8080, application=app, use_reloader=True, use_debugger=True)