# coding=utf-8
# <editor-fold desc="import packages">
import os

# <editor-fold desc="to be commented out for production code">
import sys

sys.path.append(r'C:\ProgramData\Anton Paar\Common files\scripts\src')

import pprint

pp = pprint.PrettyPrinter(indent=4)  # use pp.pprint(stuff) for pretty printing embedded list and dict
# </editor-fold>

import webbrowser

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools

import init_script
from jsonrpctcp import connect
from script_tools import tribo_port, export_excel, open_folder, info

import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt

# </editor-fold>

if __name__ == '__main__':
    # before connect to jsonrpctcp client below, open the Tribometer software (not necessary to open a testing file)
    # server side: tribometer software | client side: python script which opens jsonrpctcp connection
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
    ax.set_title("My first CoF curves")

    converted_fig = tools.mpl_to_plotly(fig)
    converted_fig['layout']['width'] = 1500
    converted_fig['layout']['height'] = 600
    info('Convert matplotlib figure to Dash figure')

    app = dash.Dash()
    app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

    app.layout = html.Div([

        dcc.Graph(
            id='CoF-curve',
            figure=converted_fig
        ),

    ], style={'width': 1500, 'margin': '30px auto'})

    info('Dash created')
    webbrowser.open_new('http://127.0.0.1:8050/')

    app.run_server(debug=False, processes=0)
    info('Dash ok')
