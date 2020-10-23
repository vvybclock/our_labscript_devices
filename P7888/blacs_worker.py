###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import user_devices.P7888.p7888_photon_counter as p7888
import ctypes

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
		
		#check to see if the P7888 (64 bit) server is running.
		settings = p7888.p7888_dll.ACQSETTING()
		returnVal = p7888.p7888_dll.GetSettingData(ctypes.pointer(settings), self.nDisplay)

		if returnVal == 0:
			raise RuntimeError("P7888 (x64) Server is not running. Please run it then restart the tab. (Swirly Arrow)")
			return False

		#DEBUG CODE IS HERE.
		p7888.set_to_sweep_mode(self.nDisplay)
		p7888.p7888_dll.NewSetting(self.nDevice)
		p7888.p7888_dll.SaveSetting()

		return True

	def program_manual(self,values):
		
		return {}

	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		#check to see if the P7888 (64 bit) server is running.
		settings = p7888.p7888_dll.ACQSETTING()
		returnVal = p7888.p7888_dll.GetSettingData(ctypes.pointer(settings), self.nDisplay)

		if returnVal == 0:
			raise RuntimeError("P7888 (x64) Server is not running. Please run it then restart the tab. (Swirly Arrow)")
			return False		

		#Set the settings on the Device.
		p7888.set_to_sweep_mode(self.nDisplay)


		# - Set the Device to respond to hardware triggers/ run in the experiment.
		self.check_before_starting()

		return {}

	def transition_to_manual(self):
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.
		self.check_before_halting()
		return True

	def shutdown(self):
		# Called once when BLACS exits
		self.check_before_halting()
		return True

	def abort_buffered(self):
		# return True
		# write_empty("_ab_buff")
		self.check_before_halting()
		return True

	def abort_transition_to_buffered(self):
		# write_empty("_ab_trans_to_buff")
		self.check_before_halting()
		return True

	def check_before_halting(self):
		status = p7888.p7888_dll.ACQSTATUS()
		p7888.p7888_dll.GetStatusData(ctypes.pointer(status), self.nDisplay)

		p7888_is_started = status.started

		if p7888_is_started:
			p7888.p7888_dll.Halt(self.nSystem)

	def check_before_starting(self):
		status = p7888.p7888_dll.ACQSTATUS()
		p7888.p7888_dll.GetStatusData(ctypes.pointer(status), self.nDisplay)

		p7888_is_not_started = not status.started

		if p7888_is_not_started:
			p7888.p7888_dll.Start(self.nSystem)