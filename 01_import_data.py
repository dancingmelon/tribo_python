# coding=utf-8
# <editor-fold desc="import packages">
import os, sys

sys.path.append(r'C:\ProgramData\Anton Paar\Common files\scripts\src')

import pprint

pp = pprint.PrettyPrinter(indent=4)  # use pp.pprint(stuff) for pretty printing embedded list and dict

import init_script
from jsonrpctcp import connect
from script_tools import tribo_port, export_excel, open_folder

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# </editor-fold>

# before connect to jsonrpctcp client below, open the Tribometer software (not necessary to open a testing file)
# server side: tribometer software | client side: python script which opens jsonrpctcp connection
tribo = connect('127.0.0.1', tribo_port)

# all available methods
tribo_methods = tribo.ls()

# the following line is used to open a tribometer testing file from python script (only with absolute file path)
# the return value is a dict with doc_id of the opened doc

tribo_doc = tribo.docs.open(path=r'C:\ProgramData\Anton Paar\InstrumX\Samples\TribometerSample.ixf')
# tribo_doc = tribo.docs.open(
#     path=r'D:\Programming\00_My_projects\2018-03-29_tribo_python\testing_files_(ixf)\Verification Doc.ixf')

# tribo.docs() for documents level methods
tribo_docs = tribo.docs()
doc_id = tribo_docs['current']
doc_name = tribo_docs['docs'][doc_id]['name']
doc_path = tribo_docs['docs'][doc_id]['path']

# tribo.groups() for groups level methods
groups = tribo.groups(doc_id=doc_id)

# tribo.parameters() for common measurement results (e.g. CoF, wear rate, Hertzian stress)
parameters_info = tribo.parameters(doc_id=doc_id)


def print_paramters(parameters):
    """
    Print out parameters information
    :param parameters:
    :return:
    """
    print "Available parameter names and units: \n"
    for i in parameters.keys():
        if (parameters[i]['unit']):
            print "Name:", parameters[i]['name'], "|", "Unit:", parameters[i]['unit']
        else:
            print "Name:", parameters[i]['name'], "|", "Unit:", "N/A"


def print_group_parameters(groups):
    """
    Print parameter values in each group and measurement
    :param groups:
    :return: None
    """
    for group_id in groups['indexes']:
        single_group = groups['groups'][group_id]
        print 'Group: ', single_group['name']
        print "***"

        for data_id in single_group['indexes']:
            data = single_group['data'][data_id]

            # IMPORTANT!!! Pay attention to the parameter loop here:
            # if there is no defined wear rate or Hertzian pressure, looping through these parameters will cause error!
            # CoF is always there, so it is safe to loop through ['0', '1000', '2000', '3000']
            for parameter_id in ['0', '1000', '2000', '3000']:
                value = tribo.parameters.getvalue(doc_id=doc_id,
                                                  data_id=data_id,
                                                  param_id=parameter_id)
                print data['name'], ':', parameters_info[parameter_id]['name'], '=', value['value'], \
                    parameters_info[parameter_id]['unit']

            print "---------------------------------------"
        print "======================================="

# get all values of a certain parameter within one group
parameters_list = tribo.parameters.getvalues(doc_id=doc_id,
                                             group_id='1',
                                             param_id='2000')

curves_info = tribo.curves(doc_id=doc_id)

# use tribo.curves.getdata(), with page_size=0, to get the data matrix shape first
# get the first measurement of groups[1] with data_id=groups['groups']['1']['indexes'][0]
curves_data_dummy = tribo.curves.getdata(doc_id=doc_id,
                                         data_id=groups['groups']['1']['indexes'][0],
                                         page_index=0,
                                         page_size=0,
                                         curve_type='ctStatic')
n_rows = curves_data_dummy['count']
n_columns = curves_data_dummy['dim_count']

# the data is always exported in SI unit, e.g. meter, second, newton, etc
curves_data = tribo.curves.getdata(doc_id=doc_id,
                                   data_id=groups['groups']['1']['indexes'][0],
                                   page_index=0,
                                   page_size=n_rows,
                                   curve_type='ctStatic')


# get the header and scale of the export curves (not completed at this time, in total 13 out of 20)
# the ScaleFactor changes dynamically according to the setting of File|Options...|Tribometer units in tribometer software
def header_and_scale_from_curve(curve_dict, index):
    key = str(index)
    if key in curve_dict:
        return [curve_dict[key]['AxisName'], curve_dict[key]['ScaleFactor']]
    else:
        return ['', 1.0]


curves_header_and_scale = [header_and_scale_from_curve(curves_info['ctStatic'], i) for i in range(n_columns)]

# My summary of all 20 headers of exported curve, all in SI unit, corresponding to raw exported data
# TODO Check R&D people for new updates in order to automatically change unit according to software setting.
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
plt.plot(np_data[:, 0], np_data[:, 16])
plt.xlabel(curves_header_complete[0])
plt.ylabel(curves_header_complete[16])
