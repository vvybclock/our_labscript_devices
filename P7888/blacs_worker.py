###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import user_devices.P7888.p7888_photon_counter as p7888
import os
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
		self.nDisplay = 0
	
		self.check_if_server_running()
		p7888.set_to_sweep_mode_via_cmd() #Set the settings on the Device.
		return True


	def program_manual(self,values):
		return {}


	def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
		''' This section is ran before the experiment runs. 

			Current (Gen 1) configuration for photon data acquisition: The photon
			counting card is set to write to a file continuously. After timeout, or
			upon reaching a certain filesize, the file is deleted, and the P7888 server is
			restarted (what does that mean?) and a  new file set up to read. 

			Testing (Gen 2) configuration for photon data acquisition: 
			Use a new file every shot.
		'''
		self.check_if_server_running()
		p7888.set_to_sweep_mode_via_cmd() #Set the settings on the Device.

		#remove old data file so we can run the P7888 without it asking about overwrites.
		if os.path.exists(p7888.p7888_data_file):
			os.remove(p7888.p7888_data_file)

		# - Set the Device to respond to hardware triggers/ run in the experiment.
		self.check_before_starting()

		return {}

	def transition_to_manual(self):
		''' 

		Here we extract data written by the P7888 server. This data file location is
		defined in set_to_sweep_mode_via_cmd().

		The bulk of this is about extracting and decoding the data. Once, decoded,
		the data needs to be partitioned into files according to the  sequence that
		ran it. This file shall then be stored in the hdf file associated with the
		shot.
		
		'''
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.

		with open(p7888.p7888_data_file, 'rb') as f:
			entire_file = f.read()
			# print(repr(entire_file))

			#determine the type of newline used: CRLF, LF, or CR
			if(b'\r\n' in entire_file):
				print("Contains CRLF")
				newline_type = 'CRLF'
				newline = b'\r\n'
			elif(b'\r' in entire_file):
				print("Contains CR")
				newline_type = 'CR'
				newline = b'\r'
			elif(b'\n' in entire_file):
				print("Contains LF")
				newline_type = 'LF'
				newline = b'\n'

			#find the start of the data and split the .lst file
			data_marker = entire_file.find(b'[DATA]')
			data_start = data_marker + len(b'[DATA]') + len(newline)
			header = entire_file[0:data_start]
			data = entire_file[data_start:]

			#convert data into integer list
			if len(data) % 4 != 0:
				print("Error: data_length isn't in 32 bit chunks")

			datalines = []
			dataints = []
			for i in range(len(data)//4):
				datalines.append(data[4*i:4*(i+1)])
				dataints.append(int.from_bytes(datalines[i], byteorder='little'))
				print(bin(dataints[i]))

			#seperate the first four bits (data is now in Most Significant Bit First).
			channels = []
			quantized_times = []
			for i in range(len(dataints)):
				channels.append(       	dataints[i] >> 30              	)
				quantized_times.append(	(0xffFFffFF >> 2) & dataints[i]	)
				print("0b{:02b}:{:030b}".format(channels[i],quantized_times[i]))



		# self.check_before_halting()
		return True

	def shutdown(self):
		# Called once when BLACS exits
		self.check_before_halting()
		return True

	def abort_buffered(self):
		''' 

		Called upon aborting a running experiment. Must return True on success.
		
		'''
		self.check_before_halting()
		return True

	def abort_transition_to_buffered(self):
		'''  

		Called upon aborting transition to buffered. Must return True on success. 

		'''
		self.check_before_halting()
		return True

	def check_if_server_running(self):
		'''Checks to see if the P7888 (64 bit) server is running.'''
		settings = p7888.p7888_dll.ACQSETTING()
		returnVal = p7888.p7888_dll.GetSettingData(ctypes.pointer(settings), self.nDisplay)
		if returnVal == 0:
			raise RuntimeError("P7888 (x64) Server is not running. Please run it then restart the tab. (Swirly Arrow)")
			return False


	def check_before_halting(self):
		''' Checks to see whether or not the P7888 device is running, 
		i.e., primed for START triggers. If it is, tell it to stop.
		'''

		status = p7888.p7888_dll.ACQSTATUS()
		p7888.p7888_dll.GetStatusData(ctypes.pointer(status), self.nDisplay)

		p7888_is_started = status.started

		if p7888_is_started:
			p7888.p7888_dll.Halt(self.nSystem)

	def check_before_starting(self):
		''' Checks to see whether or not the P7888 device is ready for 
		START triggers. If it isn't, tell it to start.
		'''

		status = p7888.p7888_dll.ACQSTATUS()
		p7888.p7888_dll.GetStatusData(ctypes.pointer(status), self.nDisplay)

		p7888_is_not_started = not status.started

		if p7888_is_not_started:
			p7888.p7888_dll.Start(self.nSystem)


if __name__ == '__main__':
	''' Testbench for checking data extraction '''
	print("In Main:")

	worker = P7888_Worker()
	worker.transition_to_manual()
