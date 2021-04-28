###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. April 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
# import user_devices.P7888.p7888_photon_counter as p7888
import numpy as np
import os
import ctypes

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker

class HP8648_Worker(Worker):
	def init(self):
		#Initialization code called once when BLACS is started. Can be used to
		#initialize the device in question and see if it's turned on, etc. and declare variables.

		#record HDF file
		self.h5_filepath = None
		self.devices = {}

		pass

	def shutdown(self):
		#Called once when BLACS exits.

		pass

	def program_manual(self,values):
		#talk to the device in question whenever a value in the GUI changes to write
		#those values in the device.

		return {}

	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		# - Access the shot file for getting hardware instructions encoded in the compilation process.
		# - Write those instructions to the device.
		# - If needed, set the device to respond to hw/sw triggers.
		# - Use initial_values to set the device to ensure continuity.
		# - The fresh variable specifies whether the entire table of instructions should be reprogrammed.
		#	- Only useful if the device supports partial programming.
		# - Return final_values. A dict holding the last values of the sequence. This allows blacs to retain
		# - output continuity after the shot is finished. 
		

		#pull the device addresses from HDF.		
		devices = self.return_devices(h5_file)

		final_values = {}
		return final_values


		#for device in device_list:
		#	print(f"VISA Address is: {device['address']}")

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
		'''
			Returns all HP8648 devices found in the HDF file and defined in the connection table as a dictionary.

			For example,

			```python
			devices = {
				
				{'dev1': 
					{'address':'blah',
					 'frequency_MHz':'blah'
					...}
				},

				{'dev2':
					...
				},
				...
			}
			```
		'''

		with h5py.File(self.h5_filepath, 'r') as hdf5_file:
			#pull out the connection table.
			connection_table = hdf5_file['/connection_table']
			print(connection_table)

			#pull out HP8648 device names and addresses


			#extract device frequencies
			# grp 	= hdf5_file[f'/devices/{self.name}/']
			# dset	= grp['frequency']
			# dset	= np.array(frequency_MHz)
			