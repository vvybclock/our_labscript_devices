###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. April 2021
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

from blacs.device_base_class import DeviceTab

class HP8648Tab(DeviceTab):
	
	def initialise_workers(self):
		#Does spelling of the function name matter? (-ize vs -ise?)

		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		# particular_setting = device.properties['particular_setting_identifier']
		gpib_address = device.properties['gpib_address']

		#Start the worker process associated with our worker class.
		#Pass it the particular settings it needs to connect.
		self.create_worker(
			'main_worker',
			'user_devices.HP8648.blacs_worker.HP8648_Worker',
			{'gpib_address' : gpib_address},
		)

		self.primary_worker = 'main_worker'