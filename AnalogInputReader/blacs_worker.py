###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import nidaqmx
import numpy as np
import os

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py
from time import sleep
#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker


VERBOSE = False
class AnalogInputReader_Worker(Worker):
	def init(self):
		print("init")
		return True


	def program_manual(self,values):
		''' This is a read only device. So this function can remain empty for now.
		'''
		print('in program_manual')
		channels = self.channels
		print(channels)
		read_value = {}
		for channel in channels:
			ch_name = channels[channel]
			try:
				with nidaqmx.Task() as task:
					task.ai_channels.add_ai_voltage_chan(ch_name)
					read_value[ch_name] = task.read()
			except Exception as e:
				print(f"Failed: {e}")
		print(read_value)
		sleep(1e-1)
		return {}


	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		''' This section is ran before the experiment runs. 
		'''
		print("In transition_to_buffered")
		channels = self.channels
		read_value = {}
		for channel in channels:
			ch_name = channels[channel]
			with nidaqmx.Task() as task:
				task.ai_channels.add_ai_voltage_chan(ch_name)
				read_value[ch_name] = task.read()
		print(read_value)
		return {}

	def transition_to_manual(self):
		''' This section is run at the end of the experiment.

		'''
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.
		print("In transition_to_manual")
		channels = self.channels
		read_value = {}
		for channel in channels:
			ch_name = channels[channel]
			with nidaqmx.Task() as task:
				task.ai_channels.add_ai_voltage_chan(ch_name)
				read_value[ch_name] = task.read()
		print(read_value)
		return True

	def shutdown(self):
		# Called once when BLACS exits
		print('in shutdown')
		return True

	def abort_buffered(self):
		''' Called upon aborting a running experiment. Must return True on success.
		'''
		print('in abort_buffered')
		return True

	def abort_transition_to_buffered(self):
		'''  Called upon aborting transition to buffered. Must return True on success. 
		'''
		print('in abort_transition_to_buffered')
		return True

if __name__ == '__main__':
	pass
