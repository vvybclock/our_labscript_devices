'''
		pyvisa was installed with command 
			`conda install -c conda-forge pyvisa`
		This installed `pyvisa-1.11.3` on our system.
'''

###########################################################################
#		Written by Chi Shu (chishu@mit.edu)	c. July 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import pyvisa


#Add in libraries for working with HDF files
# import labscript_utils.h5_lock
# import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker
from pyvisa.constants import StopBits, Parity, ControlFlow
from time import sleep
from datetime import datetime
import re
import time
from user_devices.CUAMotorMirror.scservo_sdk import *


class CUAMotorMirror_Worker(Worker):
	def init(self):
		# Read port list
		self.connected = False
		rm = pyvisa.ResourceManager()
		portslist = rm.list_resources_info()
		portsnamelist = [resourceinfo.alias for resourceinfo in  portslist.values()]
		# Check if usbport requested in portslist
		# if (self.usbport in portsnamelist):
		#	print(self.usbport)
		# else:
		#	print(portslist)
		#	# hang the tab when device is not connected
		#	raise ValueError("Device is missing")
		# # open port URT-1
		# # self.devices = PortHandler('COM4')
		# # if self.devices.setBaudRate(self.baud_rate):
		# #	print("Succeeded to change the baudrate")
		# # else:
		# #	print("Error!!!")


		# self.devices = rm.open_resource(self.usbport, read_termination = '\n',write_termination = '\n',
		#	 send_end = True, baud_rate = self.baud_rate, data_bits = 8, flow_control = ControlFlow.none, parity = Parity.none, stop_bits = StopBits.one, timeout = 25)
		# read the id number on device
		# print(self.devices.query())
		pass

	def port_lists(self):
		if not self.connected:
			rm = pyvisa.ResourceManager()
			portslist = rm.list_resources_info()
			return portslist
		else:
			return []

	def open_port(self, portname):
		'''
		open com ports
		'''
		print(portname)
		return []
		

	def shutdown(self):
		#Called once when BLACS exits.
		self.devices.close()
		pass

	def program_manual(self,values):
		#talk to the device in question whenever a value in the GUI changes to write
		#those values in the device.
		# self.spinbox_widgets[1].setValue(self.spinbox_widgets[0].Value(step*DDS_HEX)+1)
		return {}

	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		'''
		# - Access the shot file for getting hardware instructions encoded in the compilation process.
		# - Write those instructions to the device.
		# - If needed, set the device to respond to hw/sw triggers.
		# - Use initial_values to set the device to ensure continuity.
		# - The fresh variable specifies whether the entire table of instructions should be reprogrammed.
		#	- Only useful if the device supports partial programming.
		# - Return final_values. A dict holding the last values of the sequence. This allows blacs to retain
		# - output continuity after the shot is finished. 
		'''
		self.h5_filepath = h5_file
		self.device_name = device_name
	
		return {}


	def transition_to_manual(self):
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.
		
		return True

	def abort_buffered(self):
		# Called only if transition_to_buffered succeeded and the # shot if aborted prior to the initial trigger
		# return True on success
		
		return True

	def abort_transition_to_buffered(self):
		# Called only if transition_to_buffered succeeded and the # shot if aborted prior to the initial trigger
		# return True on success

		return True

	def return_devices(self, h5_filepath):
		devices = {}
		return devices

		