#####################################################################
#                                                                   #
# /user_devices/CUAMotorMirror/register_classes.py	                #
#                                                                   #
# Copyright 2021, Chi Shu MIT                                       #
#                                                                   #                           
#                                                                   #
#####################################################################
from labscript_devices import register_classes

register_classes(
    'CUAMotorMirror',
    BLACS_tab='user_devices.CUAMotorMirror.blacs_tabs.CUAMotorMirrorTab',
    runviewer_parser= None,
)
