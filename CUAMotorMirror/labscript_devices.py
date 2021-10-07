import h5py
import numpy as np
from labscript import Device, set_passed_properties, config, LabscriptError
# from math import floor

# A "labscript_device" is what one defines in the connection table. It's how
# labscript knows how to drive the device. Here we are defining an
# "unbuffered" device. Something that runs on its own CPU time, and  something
# we just need to send data to every so often. It's interface is not timing
# critical.

###########################################################################
#		Written by Chi Shu (chishu@mit.edu)	c. July 2021	
###########################################################################


class CUAMotorMirror(Device):
	''' A labscript device for sending frequency setpoints. '''

	# Labscript REQUIRED Commands Here

	# This decorator declares that some keyword arguments should be saved to the
	# connection table, so that BLACS can read them:
	@set_passed_properties({'connection_table_properties' : ['usbport', 'baud_rate']})
	def __init__(self, name, usbport, baud_rate = 500000):
		Device.__init__(self, name = name, parent_device = None, connection = None)
		# BlACS connection
		self.BLACS_connection = usbport


	def generate_code(self,hdf5_file):
		''' Parse commands and timings and save the correct sequence into HDF file.
		'''
		# grp	= hdf5_file.require_group(f'/devices/{self.name}/')
		

