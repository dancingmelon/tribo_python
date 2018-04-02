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

from flask import Flask, render_template
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

    app.layout = html.Div([

        html.H1("This is a iframe of babylon.js asset!!!"),

        html.Iframe(
            src='/babylon',
            style={
                'display': 'inline-block',
                'width': '800px',
                'height': '400px'
            }
        ),

        html.H1(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montreal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])


    @server.route('/babylon')
    def babylon():
        return render_template('index.html')


    # add webbrowser.open_new('http://127.0.0.1:5000/') in production code
    # change this to server.run(debug=False, processes=0) in production code

    server.run(debug=True)
