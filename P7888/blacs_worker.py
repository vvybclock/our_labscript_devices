###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import user_devices.P7888.p7888_photon_counter as p7888

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker



class TemplateWorker(Worker):
	def init(self):
		#Initialization code called once when BLACS is started. Can be used to
		#initialize the device in question and see if it's turned on, etc.

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

def write_empty(fname):
	with open(r'C:\Users\Boris\labscript-suite\userlib\user_devices\P7888' + '\\' + fname + '.txt', 'w') as fp:
		pass

class P7888_Worker(Worker):
	def init(self):
		#define variable placeholders for the worker.
		self.shot_file = None
		# write_empty('_p7888_worker_init_ran')

		return True

	def program_manual(self,values):
		# write_empty('_p7888_worker_program_manual_ran')
		return {}

	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		# - Set the Device to respond to hardware triggers.
		# p7888_dll.Start()
		# write_empty('_p7888_trans_to_buf_ran')
		return {}

	def transition_to_manual(self):
		# p7888_dll.Halt()
		# write_empty('_trans_to_man_ran')
		return True

	def shutdown(self):
		# write_empty("_shutdown")
		return True

	def abort_buffered(self):
		# return True
		# write_empty("_ab_buff")
		pass

	def abort_transition_to_buffered(self):
		# write_empty("_ab_trans_to_buff")
		return True