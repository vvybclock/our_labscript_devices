###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker


class TemplateWorker(Worker):
	def init(self):
		pass

	def program_manual(self,values):
		pass

	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		pass

	def transition_to_manual(self):
		pass

	def shutdown(self):
		pass

	def abort_buffered(self):
		pass

	def abort_transition_to_buffered(self):
		pass

class P7888_Worker(Worker):
	def init(self):
		pass