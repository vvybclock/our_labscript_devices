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
# import numpy as np
# import math


#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker
from pyvisa.constants import StopBits, Parity, ControlFlow
from time import sleep


class FPGA_DDS_Worker(Worker):
	def init(self):
		#Initialization code called once when BLACS is started. Can be used to
		#initialize the device in question and see if it's turned on, etc. and declare variables.

		#record HDF file
		self.h5_filepath = None
		# clock frequency of AD9959
		self.ClockRate = 480*10**6
		# number of bits for frequency word
		self.freqbits = 32
		# number of bits for phase word
		self.phasbits = 14
		# 
		self.ampbits = 10 
		self.devices = {}
		self.singlefunction = {"freq": self.SingleFrequencySet,
								"pha": self.SinglePhaseSet,
								"amp": self.SingleAmplitudeSet}

		# Read port list
		rm = pyvisa.ResourceManager()
		portslist = rm.list_resources_info()
		portsnamelist = [resourceinfo.alias for resourceinfo in  portslist.values()]
		# Check if usbport requested in portslist
		if (self.usbport in portsnamelist):
			print(self.usbport)
		else:
			print(portsnamelist)
			# hang the tab when device is not connected
			raise ValueError("Device is missing")
		# open FPGA_DDS device UART
		self.devices = rm.open_resource(self.usbport, read_termination = '\n',write_termination = '\n',
			 send_end = True, baud_rate = 230400, data_bits = 8, flow_control = ControlFlow.none, parity = Parity.none, stop_bits = StopBits.one, timeout = 25)
		# read the id number on device
		print(self.devices.query("?id"))
		
		self.FPGAReset()
		self.ExternalTrigger()
		self.ReferenceTrigger()
		# 'ASRL5::INSTR': ResourceInfo(interface_type=<InterfaceType.asrl: 4>, interface_board_number=5, resource_class='INSTR', resource_name='ASRL5::INSTR', alias='FPGA_DDS9')
		self.singlefunction["freq"](0, 83*10**6) # set channel 0 frequency to 80MHz
		self.singlefunction["pha"](0, 0) # set channel 0 phase to 0degree
		self.singlefunction["amp"](0, 0.15) # set channel 0 amplitude to 0.15

		self.singlefunction["freq"](1, 83*10**6) # set channel 0 frequency to 80MHz
		self.singlefunction["pha"](1, 0) # set channel 0 phase to 0degree
		self.singlefunction["amp"](1, 0.15) # set channel 0 amplitude to 0.15


		self.singlefunction["freq"](2, 83*10**6) # set channel 0 frequency to 80MHz
		self.singlefunction["pha"](2, 0) # set channel 0 phase to 0degree
		self.singlefunction["amp"](2, 0.15) # set channel 0 amplitude to 0.15


		self.singlefunction["freq"](3, 83*10**6) # set channel 0 frequency to 80MHz
		self.singlefunction["pha"](3, 0) # set channel 0 phase to 0degree
		self.singlefunction["amp"](3, 0.15) # set channel 0 amplitude to 0.15

		pass

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

		if np.isnan(self.frequency_MHz):
			print("No Set Frequency. Doing nothing...")
		else:
			print(f"Set Frequency (MHz): {self.frequency_MHz}")
			print("\tSetting Frequency...")
			#set frequency
			# self.set_frequency()
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
			Returns all FPGA_DDS devices found in the HDF file and defined in the connection table as a dictionary.

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
			
			#pull out FPGA_DDS device names and addresses
			for line in connection_table:
				#check to see if the class is correct.
				if line[1].decode('ascii') == 'FPGA_DDS':
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

	def MasterReset(self): # testing!!!!!!!!
		#Software to FPGA to Master Reset AD9959
		print(self.devices.query("!AD9959Init"))

	def FPGAReset(self):
		# Disarm FPGA
		self.devices.write("!FPGADDSRESET")
		sleep(0.003)

	def ExternalTrigger(self):
		# Set Trigger to External
		print(self.devices.query("!ExtT"))

	def ReferenceTrigger(self):
		# set Reference output to Trigger
		print(self.devices.query("!RefT"))

	def SingleFrequencySet(self, channel, data):
		# set single channel frequency. This function will reset FPGA DDS control logic and disarm FPGA
		message = channel<<4 | 0x00
		data = round(data/self.ClockRate*2**self.freqbits % (2**self.freqbits))
		print(self.devices.query("!ChSet"))
		self.devices.write_raw(b''.join(
			[message.to_bytes(1, byteorder = 'big' ),
			 data.to_bytes(4, byteorder = 'big' ),
			  b'\x0a']))
		print(self.devices.read())

	def SinglePhaseSet(self, channel, data):
		message = (channel<<4) | 0x01
		data = round(data/360*2**self.phasbits % (2**self.phasbits))
		print(self.devices.query("!ChSet"))
		self.devices.write_raw(b''.join(
			[message.to_bytes(1, byteorder = 'big' ),
			 data.to_bytes(4, byteorder = 'big' ),
			  b'\x0a']))
		print(self.devices.read())
		
	def SingleAmplitudeSet(self, channel, data):
		message = channel<<4 | 0x02
		data = round(data/1*(2**self.ampbits-1) % (2**self.ampbits)) | 1<<12
		print(self.devices.query("!ChSet"))
		self.devices.write_raw(b''.join(
			[message.to_bytes(1, byteorder = 'big' ),
			 data.to_bytes(4, byteorder = 'big' ),
			  b'\x0a']))
		print(self.devices.read())
		