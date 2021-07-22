#####################################################################
#                                                                   #
# /user_devices/FPGA_DDS/register_classes.py               #
#                                                                   #
# Copyright 2021, Chi Shu MIT               #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
from labscript_devices import register_classes

register_classes(
    'FPGA_DDS',
    BLACS_tab='user_devices.FPGA_DDS.blacs_tabs.FPGA_DDSTab',
    runviewer_parser='user_devices.FPGA_DDS.runviewer_parser.FPGA_DDSParser',
)
