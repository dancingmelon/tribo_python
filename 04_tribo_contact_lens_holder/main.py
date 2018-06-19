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
from plotly import tools

import init_script
from jsonrpctcp import connect
from script_tools import tribo_port, export_excel, open_folder, info

import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt

# </editor-fold>

if __name__ == '__main__':
    server = Flask(__name__)
    app = dash.Dash(__name__, server=server)

    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    # app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    tribo = connect('127.0.0.1', tribo_port)

    result = tribo.ls()
    info('Connected to {}, {}'.format(result['server_name'], result['server_version']))

    tribo_docs = tribo.docs()
    doc_id = tribo_docs['current']
    doc_name = tribo_docs['docs'][doc_id]['name']
    info('Opened document: {}'.format(doc_name))

    groups = tribo.groups(doc_id=doc_id)
    info('Opened groups')

    curves_data_dummy = tribo.curves.getdata(doc_id=doc_id,
                                             data_id=groups['groups']['1']['indexes'][0],
                                             page_index=0,
                                             page_size=0,
                                             curve_type='ctStatic')
    n_rows = curves_data_dummy['count']
    n_columns = curves_data_dummy['dim_count']
    info('Get dimension of first measurement: {} rows by {} columns'.format(n_rows, n_columns))

    curves_data = tribo.curves.getdata(doc_id=doc_id,
                                       data_id=groups['groups']['1']['indexes'][0],
                                       page_index=0,
                                       page_size=n_rows,
                                       curve_type='ctStatic')

    curves_header_complete = [
        u"Time [s]",
        u"Sliding Time [s]",
        u"Cycles Reset",
        u"Cycles Recompute",
        u"Distance [m]",
        u"Linear Position [m]",
        u"Angular Position [rad]",
        u"Speed [m/s]",
        u"Normal Force [N]",
        u"Friction Force [N]",
        u"Penetration Depth [m]",
        u"Oven Temperature [°C]",
        u"Sample Temperature [°C]",
        u"User Channel 1",
        u"User Channel 2",
        u"User Channel 3",
        u"Coefficient of Friction",
        u"Max Linear Speed [m/s]",
        u"Norminal Normal Force [N]",
        u"Sequence Count"
    ]

    # make numpy matrix and plot CoF
    np_data = np.array(curves_data['data'])
    info('Get data into numpy array, shape: ({}x{})'.format(np_data.shape[0], np_data.shape[1]))

    info('Set up matplotlib curves')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np_data[:, 0], np_data[:, 16])
    ax.set_xlabel(curves_header_complete[0])
    ax.set_ylabel(curves_header_complete[16])
    ax.xaxis.label.set_size(16)
    ax.yaxis.label.set_size(16)
    # ax.set_title("My first CoF curves")

    converted_fig = tools.mpl_to_plotly(fig)
    converted_fig['layout']['width'] = 1100
    converted_fig['layout']['height'] = 500
    info('Convert matplotlib figure to Dash figure')

    app.layout = html.Div([

        html.Link(
            rel='stylesheet',
            href='/static/css/dash_official_stylesheet.css'
        ),

        # dcc.Location(id='url', refresh=False),

        html.Div(html.H2("3D Visualisation of Contact Lens Holder"),
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

        html.H2("Friction Curve",
                style={
                    'textAlign': 'center'
                }),

        dcc.Graph(
            id='CoF-curve',
            figure=converted_fig
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
