###############################################
# 
# /user_devices/FPGA_DDS/runviewer_parser.py     
# Copyright 2021  Chi Shu MIT
# This is the file display traces for FPGA_DDS
# Modify runviewer\_main_.py add_trace function add a line 
        # if con is None:
        #     return
# before con.device_class
# not sure how to implement it without change the original labscript codes
###############################################


from labscript_devices import runviewer_parser 
from labscript import LabscriptError
import h5py
import numpy as np
    
@runviewer_parser
class FPGA_DDSParser(object):
	def __init__(self, path, device):
		self.path = path
		self.name = device.name
		self.device = device

	def get_traces(self, add_trace, clock = None):
		with h5py.File(self.path, 'r') as f:
			instructions = f['/devices/'+self.name+'/Instructions']
			Time = instructions["Time"]
			Ch = instructions["Ch"]
			Func = instructions["Func"]
			RampRate = instructions["RampRate"]
			Data = instructions["Data"]
			print(Time)
			print(Ch)
			print(Func)
			print(RampRate)
			print(Data)
			

		try:
			add_trace('FPGA_test',([0.1, 0.2, 0.5],[80*10**6,83*10**6,80*10**6]), self.name, 'test2')
		except Exception as e:
			print(e)
			sys.stdout = sys.__stdout__
		else:
			pass
		finally:
			pass	
		# This device don't trigger any other devices
		trigger = {}
		return trigger

    



