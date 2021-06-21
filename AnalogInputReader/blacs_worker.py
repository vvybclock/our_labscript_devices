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
		return True


	def program_manual(self,values):
		''' This is a read only device. So this function can remain empty for now.
		'''

		return {}


	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		''' This section is ran before the experiment runs. 
		'''

		return {}

	def transition_to_manual(self):
		''' This section is run at the end of the experiment.

		'''
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.

		return True

	def shutdown(self):
		# Called once when BLACS exits
		return True

	def abort_buffered(self):
		''' Called upon aborting a running experiment. Must return True on success.
		'''
		return True

	def abort_transition_to_buffered(self):
		'''  Called upon aborting transition to buffered. Must return True on success. 
		'''
		return True

if __name__ == '__main__':
	pass
