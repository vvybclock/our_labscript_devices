import h5py
import numpy as np
from labscript import Device, set_passed_properties


# A "labscript_device" is what one defines in the connection table. It's how
# labscript knows how to drive the device. Here we are defining an
# "unbuffered" device. Something that runs on its own CPU time, and  something
# we just need to send data to every so often. It's interface is not timing
# critical.




class FPGA_DDS(Device):
	''' A labscript device for sending frequency setpoints. '''

	frequency_MHz = None

	# Labscript REQUIRED Commands Here

	# This decorator declares that some keyword arguments should be saved to the
	# connection table, so that BLACS can read them:
	@set_passed_properties({'connection_table_properties' : ['usbport']})
	def __init__(self, name, usbport):

		Device.__init__(self, name=name, parent_device=None,connection=usbport)

		# The existence of this attribute is how BLACS knows it needs to make a tab for
		# this device:
		# STILL, HOW DOES BLACS KNOW WHERE TO FIND THE TAB CLASS????
		# It uses register_classes.py, which it's defined to scan for.
		self.BLACS_connection = usbport

	#labscript optional? commands here.

	def generate_code(self,hdf5_file):
		''' Simply saves the set point for the FPGA_DDS frequency in the HDF.
		'''
		grp 	= hdf5_file.require_group(f'/devices/{self.name}/')
		dset	= grp.require_dataset('frequency',(1,),dtype='f')
		
		if self.frequency_MHz != None:
			dset[0]	= self.frequency_MHz
		else:
			dset[0] = np.nan
		

	def constant(self, frequency_MHz):
		''' Just save the frequency for compilation later. 
		'''
		self.frequency_MHz = frequency_MHz
		pass