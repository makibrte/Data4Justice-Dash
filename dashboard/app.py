# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import datetime
import io
import base64

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Load data and clean the data here:
# load data from api
# Create the app layout here:
app.layout = html.Div([
    html.H1("Data Visualization Options", style={'text-align': 'center'}),
    html.H2("Select a visualization type:", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Box Plot', 'value': 'box'},
            {'label': 'Geo Map', 'value': 'map'}
        ],
        value='line',
        style={'width': '50%', 'display': 'inline-block', 'margin-left': '25%'}
    ),
    dcc.Graph(id='graph'),

    html.Div([
        html.H1("Upload your file here:", style={'text-align': 'left'}),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        html.Div(id='output-data-upload2')
    ])

])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown):
    if dropdown == 'line':
        fig = px.line()
    elif dropdown == 'bar':
        fig = px.bar()
    elif dropdown == 'scatter':
        fig = px.scatter()
    elif dropdown == 'histogram':
        fig = px.histogram()
    elif dropdown == 'box':
        fig = px.box()
    elif dropdown == 'map':
        fig = px.scatter_geo()
    return fig


@app.callback(
    dash.dependencies.Output('output-data-upload', 'children'),
    [dash.dependencies.Input('upload-data', 'contents')],
    [dash.dependencies.State('upload-data', 'filename'),
     dash.dependencies.State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def parse_contents(contents, filename, date):
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
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
    ])


# Create the callback function here:

if __name__ == '__main__':
    app.run_server(debug=True)
