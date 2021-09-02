'''
		pyvisa was installed with command 
			`conda install -c conda-forge pyvisa`
		This installed `pyvisa-1.11.3` on our system.
'''

###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. April 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import pyvisa
import numpy as np


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
		self.h5_filepath = h5_file
		self.device_name = device_name

		#pull the device addresses from HDF.		
		devices = self.return_devices(h5_file)

		self.frequency_MHz	= devices[device_name]['frequency_MHz']
		self.address      	= devices[device_name]['address']
		print(self.frequency_MHz)
		if np.isnan(self.frequency_MHz):
			print("No Set Frequency. Doing nothing...")
		else:
			print(f"Set Frequency (MHz): {self.frequency_MHz}")
			print("\tSetting Frequency...")
			#set frequency
			self.set_frequency()
			print("Done!")


		final_values = {}
		return final_values


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
		devices = {}

		with h5py.File(self.h5_filepath, 'r') as hdf5_file:
			#pull out the connection table.
			connection_table = hdf5_file['/connection table']
			
			#pull out HP8648 device names and addresses
			for line in connection_table:
				#check to see if the class is correct.
				if line[1].decode('ascii') == 'HP8648':
					device_name	= line[0].decode('ascii')
					address    	= line[6].decode('ascii')

					#save parameters
					devices[device_name] = {'address': address}
			
			#extract device frequencies
			for device_name in devices:
				frequency_dset = hdf5_file[f'/devices/{device_name}/frequency']
				#store into `devices`
				devices[device_name]['frequency_MHz'] = frequency_dset[0]
			pass

		return devices

	def set_frequency(self):
		''' Sets frequency using the locally defined variables and with the help of
		the pyVISA library.  '''
		rm = pyvisa.ResourceManager("C:\\Windows\\System32\\visa64.dll")
		# rm = pyvisa.ResourceManager()
		all_addresses = rm.list_resources()

		if self.address in all_addresses:
			hp8648 = rm.open_resource(self.address)
			cmd = f"FREQ:CW {self.frequency_MHz} MHZ"
			print(f"\tGPIB Command: {cmd}")

			return_val = hp8648.write(cmd)
			print(f"\tReturn Value: {return_val}")
		pass
