# <editor-fold desc="import packages">
import os, sys

sys.path.append(r'C:\ProgramData\Anton Paar\Common files\scripts\src')

from pprint import pprint as pp

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
pp(tribo_methods)

# the following line is used to open a tribometer testing file from python script (only with absolute file path)
tribo.docs.open(path=r'C:\ProgramData\Anton Paar\InstrumX\Samples\TribometerSample.ixf')
# tribo.docs.open(path=r'C:\WORKSPACE\2_Product\5_Software\Python\tribo_python\testing_files_ixf\SimpleExample.ixf')


# tribo.docs() for documents level methods
tribo_docs = tribo.docs()
pp(tribo_docs)
doc_id = tribo_docs['current']
doc_name = tribo_docs['docs'][doc_id]['name']
doc_path = tribo_docs['docs'][doc_id]['path']

# tribo.groups() for groups level methods
groups = tribo.groups(doc_id=doc_id)
pp(groups)

# tribo.parameters() for common measurement results (e.g. CoF, wear rate, Hertzian stress)
parameters = tribo.parameters(doc_id=doc_id)
pp(parameters)


def print_paramters(parameters):
    print "Available parameter names and units: \n"
    for i in parameters.keys():
        if (parameters[i]['unit']):
            print "Name:", parameters[i]['name'], "|", "Unit:", parameters[i]['unit']
        else:
            print "Name:", parameters[i]['name'], "|", "Unit:", "N/A"


print_paramters(parameters)


# Output:
# Name: Partner Wear Rate | Unit: mm³/(N·m)
# Name: Max Herzian Stress | Unit: GPa
# Name: Sample Wear Rate | Unit: mm³/(N·m)
# Name: Min µ | Unit: N/A
# Name: Mean µ | Unit: N/A
# Name: StdDev µ | Unit: N/A
# Name: Max µ | Unit: N/A


# Print parameter values in each group and measurement
def print_group_parameters(groups):
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
                print data['name'], ':', parameters[parameter_id]['name'], '=', value['value'], \
                    parameters[parameter_id]['unit']

            print "---------------------------------------"
        print "======================================="


print_group_parameters(groups)

curves = tribo.curves(doc_id=doc_id)
pp(curves)


