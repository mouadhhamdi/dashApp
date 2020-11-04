import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash_extensions import Download
import base64
import io

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

layout = html.Div([
    dcc.Upload(
            id='datatable-upload',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files to upload')
            ]),
            style={
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
            },
        ),
    html.Br(),
    html.H1("Last data version"),
    dash_table.DataTable(
        id='table-editing',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
        ],
        editable=True,
        row_deletable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action='native',
        page_size=10,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

    ),
    html.Div(id='table-editing-hidden-output'),
    dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="graph"),
    html.Br(),


    Download(id="download"),
    html.Div([
        dbc.Button('Save data and run model', id='save-data', color="danger", className="mr-1", size="lg"),
        dbc.Button("Download data", id="btn")
    ])


])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df.to_dict('records')