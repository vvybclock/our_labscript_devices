###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

from blacs.device_base_class import DeviceTab

class AnalogInputReaderTab(DeviceTab):
	
	def initialise_workers(self):
		#Does spelling of the function name matter? (-ize vs -ise?)

		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		# particular_setting = device.properties['particular_setting_identifier']
		channels = device.properties['channels']

		#Start the worker process associated with our worker class.
		#Pass it the particular settings it needs to connect.
		self.create_worker(
			'main_worker',
			'user_devices.AnalogInputReader.blacs_worker.AnalogInputReader_Worker',
			{'channels' : channels},
		)

		self.primary_worker = 'main_worker'

	def initalise_GUI(self):

		pass

	def get_channels(self):
		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		self.channels = device.properties['channels']