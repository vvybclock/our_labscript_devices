'''
use serial command instead of pyvisa
'''

###########################################################################
#		Written by Chi Shu (chishu@mit.edu)	c. July 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
# import pyvisa
# from pyvisa.constants import StopBits, Parity, ControlFlow


#Add in libraries for working with HDF files
# import labscript_utils.h5_lock
# import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker
from time import sleep
from datetime import datetime
import re
import time
import os
import serial.tools.list_ports
from user_devices.CUAMotorMirror.scservo_sdk import *
from user_devices.CUAMotorMirror.CUAMotors import *

DeviceFilepath = os.path.dirname(os.path.realpath(__file__))

class CUAMotorMirror_Worker(Worker):
	def init(self):
		# Read port list
		self.connected = False
		self.portname = None
		self.device = None
		self._baud = 500000
		self._protocol_end = 0
		self._baud = self.baud_rate

		self.IDs = []
		self.motors = []
		# self.open_port(self.usbport)
		# self.search_motors()
		# print(self.IDs)


	def open_port(self, portname):
		'''
		open com ports
		ask user to select a port from pop dialog or use preselected value
		'''
		assert (self.connected == False)
		# read all com port
		ports = serial.tools.list_ports.comports()
		portnamelist = [port for port, desc, hwid in sorted(ports)]
		print(portnamelist)
		# open port
		if portname in portnamelist:
			self.portname = portname
			portHandler = PortHandler(self.portname)
			packetHandler = PacketHandler(self._protocol_end)
			if portHandler.setBaudRate(self._baud): # this command open port
				print("Succeeded to set baud and open_port")
				self.device = portHandler
				self.packetHandler = packetHandler
				self.connected = True
				return True
			else:
				print("Failed to change baud or open_port")
				raise "Failed to open Motor port" 
				quit()
				return False
		else: 
			return False

	def search_motors(self):
		print("search Motors")
		assert (self.connected == True)
		IDs = []
		motors = []
		for searchID in range(1, 50):
			print(searchID)
			scs_model_number, scs_comm_result, scs_error = self.packetHandler.ping(self.device, searchID)
			if (scs_comm_result == COMM_SUCCESS) and (scs_error==0):
				IDs.append(searchID)
				

		self.IDs = IDs		
		return IDs

	def MotorIDs(self):
		return self.IDs
		
	def close_port(self):
		self.device.closePort()
		return True

	def shutdown(self):
		#Called once when BLACS exits.
		self.close_port()
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

		