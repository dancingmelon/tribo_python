# coding=utf-8
# <editor-fold desc="import packages">
import os

import sys

sys.path.append(r'C:\ProgramData\Anton Paar\Common files\scripts\src')
sys.path.append(r'C:\ProgramData\Anton Paar - Beta\Common files\scripts\src')

# <editor-fold desc="to be commented out for production code">
import pprint
pp = pprint.PrettyPrinter(indent=4)  # use pp.pprint(stuff) for pretty printing embedded list and dict
# </editor-fold>

import webbrowser

from flask import Flask, render_template, send_from_directory
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
# import plotly.graph_objs as go
# import plotly.figure_factory as ff
# from plotly import tools

import init_script
from jsonrpctcp import connect
from script_tools import tribo_port, export_excel, open_folder, info

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# </editor-fold>

if __name__ == '__main__':
    server = Flask(__name__)
    app = dash.Dash(__name__, server=server)

    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    # app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
    app.layout = html.Div([

        html.Link(
            rel='stylesheet',
            href='/static/css/dash_official_stylesheet.css'
        ),

        # dcc.Location(id='url', refresh=False),

        html.Div(html.H2("3D Visualisation of Tribometer"),
                 style={'textAlign': 'center'}),

        # html.Br(),

        html.Iframe(
            src='/babylon',
            style={
                'display': 'inline-block',
                'width': '1100px',
                'height': '600px'
            }
        ),

        html.Div(html.A('Click for full screen',
                        href="http://127.0.0.1:5000/babylon",
                        className='button button-primary'),
                 className='row',
                 style={'textAlign': 'center'}),

        # dcc.Link('Click for full screen', href='http://127.0.0.1:5000/babylon'),

        html.Hr(),

        html.H2("Dash: A web application framework for Python",
                style={
                    'textAlign': 'center'
                }),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montreal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization',
                    'width': 1100,
                    'height': 600
                }
            }
        )
    ], className="container")


    @server.route('/babylon')
    def babylon():
        return render_template('index.html')

    @server.route('/static/<path:path>')
    def static_file(path):
        static_folder = os.path.join(os.getcwd(), 'static')
        return send_from_directory(static_folder, path)

    # add webbrowser.open_new('http://127.0.0.1:5000/') in production code
    # change this to server.run(debug=False, processes=0) in production code

    server.run(debug=True)
