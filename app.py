import dash
import dash_auth
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from manual_updates import layout as manual_update_layout
from nav_bar import layout as nav_bar_layout
from flask import Flask
from authentication import VALID_USERNAME_PASSWORD_PAIRS
from manual_updates import parse_contents
from dash_extensions.snippets import send_data_frame

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

server = Flask(__name__)
app = dash.Dash(
    server=server,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/brPBPO.css",
        dbc.themes.BOOTSTRAP
    ],
    url_base_pathname='/cof/dash/'
)
app.suppress_callback_exceptions=True

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.layout = nav_bar_layout

# empty output I just need data
@app.callback(
    Output('table-editing', 'data'),
    [Input('datatable-upload', 'contents')],
    [State('datatable-upload', 'filename')])
def display_output(list_of_contents, list_of_names):
    if list_of_contents is None:
        return df.to_dict('records')
    else:
        return parse_contents(list_of_contents, list_of_names)

@app.callback(
    Output('loading-1', 'children'),
    [Input('save-data', 'n_clicks')],
    [State('table-editing', 'data'),
    State('table-editing', 'columns')])
def save_table(n_clicks, rows, columns):
    import time
    if n_clicks is not None and n_clicks > 0:
        df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        print(df)
        time.sleep(5)

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return False, True, False
    print(pathname)
    return [pathname == f"/cof/dash/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/cof/dash/", "/cof/dash/page-1"]:
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/cof/dash/page-2":
        return manual_update_layout
    elif pathname == "/cof/dash/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def func(n_nlicks):
    if n_nlicks is not None:
        return send_data_frame(df.to_csv, "data.csv")


if __name__ == '__main__':
    app.run_server(debug=False)
