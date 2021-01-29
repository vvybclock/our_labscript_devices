###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

#Add in libraries for communicating with the device
import user_devices.P7888.p7888_photon_counter as p7888
import numpy as np
import os
import ctypes

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add in labscript_classes for defining the worker process.
from blacs.tab_base_classes import Worker

#timer
import time



class TemplateWorker(Worker):
	def init(self):
		#Initialization code called once when BLACS is started. Can be used to
		#initialize the device in question and see if it's turned on, etc. and declare variables.

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


#OPERATION_MODE = 'GEN1'
OPERATION_MODE = 'GEN2'
FILESIZE_LIMIT_IN_BYTES = 100000000
VERBOSE = False
class P7888_Worker(Worker):
	def init(self):
		#define variable placeholders for the worker.
		self.shot_file = None
		self.nDisplay = 0
		self.h5_filepath = None

		#perform P7888 initilizations
		self.check_if_server_running()
		p7888.set_to_sweep_mode_via_cmd() #Set the settings on the Device.
		return True


	def program_manual(self,values):
		''' The P7888 is a read only device. So this function can remain empty for now.

		Possible Future expansion would give options for changing the photon counter
		settings in BLACS. Which isn't necessary right now.
		'''
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
		self.start_time = time.time()
		self.h5_filepath = h5_file

		if OPERATION_MODE == 'GEN2':
			self.check_if_server_running()
			p7888.set_to_sweep_mode_via_cmd() #Set the settings on the Device.

			#remove old data file so we can run the P7888 without it asking about overwrites.
			if os.path.exists(p7888.p7888_data_file):
				os.remove(p7888.p7888_data_file)

			# - Set the Device to respond to hardware triggers/ run in the experiment.
			self.check_before_starting()
		elif OPERATION_MODE == 'GEN1':
			self.check_if_server_running()
			p7888.set_to_sweep_mode_via_cmd() #Set the settings on the Device.

			#delete the current file if and only if we're currently running the data taking.
			was_running = self.check_before_starting()
			if not was_running and os.path.exists(p7888.p7888_data_file):
				os.remove(p7888.p7888_data_file)
			
		self.end_transition_time = time.time()
		print(f"Time to Start: {self.end_transition_time - self.start_time:.2}")
		try:
			print(f"Time since since last run: {self.end_transition_time - self.experiment_end_time:.2}")
		except:
			pass
		return {}

	def transition_to_manual(self):
		''' This section is run at the end of the experiment.

		Here we extract data written by the P7888 server. This data file location is
		defined in set_to_sweep_mode_via_cmd(). See 'transition_to_buffered'.

		The bulk of this is about extracting and decoding the data written by the
		P7888 onto the harddrive. Once, decoded, the data needs to be partitioned
		into smaller 'files' according to the  sequence that ran it. This file shall
		then be stored in the hdf file associated with the shot.
		
		Rather than perform this complicated, and lab generational difference here, 
		we shall simply copy the whole file into the HDF. And write a seperate bit
		of  analysis code to split the file. This should maintain better code, and
		make it easier to modify in the future.
		
		In this function, we'll save a boolean variable:
		'is_photon_arrivals_processed', the entire photon arrival times file, and
		the file from the previous run. This should facilitate easier dissection of
		the data into smaller chunks. 
		'''
		# - Called after shot is finished.
		# - The device should be placed in manual mode here.
		# - Useful for saving data.
		# - Return True on success.

		# data_file = r'C:\Users\Boris\labscript-suite\userlib\user_devices\P7888\sample_data.lst'
		# with open(data_file, 'rb') as f:
		with open(p7888.p7888_data_file, 'rb') as f:
			entire_file = f.read()

		newline_type, newline    	= self.determine_newline_type(entire_file)
		header, data             	= self.split_file_into_header_and_data(entire_file, newline)
		channels, quantized_times	= self.decode_data(data=data, verbose=VERBOSE)
		header_dict              	= self.decode_header(header, verbose=VERBOSE)

		#store 'all_arrivals' to HDF file.
		with h5py.File(self.h5_filepath,'a') as hdf:
			#create folder for photon counts
			grp = hdf.create_group("/data/photon_arrivals")
			file_array = np.fromfile(p7888.p7888_data_file,dtype='<i4')
			lst_file = grp.create_dataset("all_arrivals",data=file_array)
			lst_file.attrs.create("Description", data=
				'Contains the very large photon arrival file. This file contains the data of arrival times from multiple shots. Not just the one shot we care about here.'
			)


		if OPERATION_MODE == 'GEN2':
			self.check_before_halting()

		#erase p7888.p7888_data_file if too large.
		file_size_in_bytes = os.stat(p7888.p7888_data_file).st_size
		if file_size_in_bytes > FILESIZE_LIMIT_IN_BYTES:
			self.check_before_halting()
			if os.path.exists(p7888.p7888_data_file):
				os.remove(p7888.p7888_data_file)

		self.experiment_end_time = time.time()
		return True

	def shutdown(self):
		# Called once when BLACS exits
		self.check_before_halting()
		return True

	def abort_buffered(self):
		''' Called upon aborting a running experiment. Must return True on success.
		'''
		self.check_before_halting()
		return True

	def abort_transition_to_buffered(self):
		'''  Called upon aborting transition to buffered. Must return True on success. 
		'''
		self.check_before_halting()
		return True

#============================================#
#	Helper Functions ---- Helper Functions   #
#	****** Helper Functions Below ********   #
#============================================#

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

		Returns whether or not it was running.
		'''

		status = p7888.p7888_dll.ACQSTATUS()
		p7888.p7888_dll.GetStatusData(ctypes.pointer(status), self.nDisplay)

		p7888_is_not_started = not status.started

		if p7888_is_not_started:
			p7888.p7888_dll.Start(self.nSystem)

		return status.started

	def determine_newline_type(self, entire_file):
		'''newline_type, newline = determine_newline_type(entire_file)

		Reads a whole file in as a string and returns newline type as string 'CRLF',
		'CR', 'LF' as well as the newline string.
		'''
		if(b'\r\n' in entire_file):
			if VERBOSE: print("Contains CRLF") 
			newline_type = 'CRLF'
			newline = b'\r\n'
		elif(b'\r' in entire_file):
			if VERBOSE: print("Contains CR") 
			newline_type = 'CR'
			newline = b'\r'
		elif(b'\n' in entire_file):
			if VERBOSE: print("Contains LF")
			newline_type = 'LF'
			newline = b'\n'

		return (newline_type, newline)

	def split_file_into_header_and_data(self, entire_file, newline):
		''' header, data = split_file_into_header_and_data(entire_file, newline) 

		Reads entire file to find the start of the data '[DATA]' and
		then looks a newline after it to find the datastream.
		'''

		#find the start of the data and split the .lst file
		data_marker = entire_file.find(b'[DATA]')
		data_start = data_marker + len(b'[DATA]') + len(newline)
		header = entire_file[0:data_start]
		data = entire_file[data_start:]

		return header, data

	def decode_data(self, data,verbose=False):
		''' channels, quantized_times = decode_data(data)
		
		Deconverts the bytes into python-computable integer lists. Data is encoded 
		as a LSB first and as decoded as such.

		Channel Values are from 0 to 3 inclusive. Denoting the 4 input channels.
		The Start events are encoded in one of these channels, and denoted by
		the 0 timing and non-zero channel.

		Quantized times are in units found in the header file.

		Verbose print's the decoded data in binary format.
		'''

		if len(data) % 4 != 0:
			raise RuntimeError("Error: P7888 data isn't in 32 bit chunks")

		number_of_32_bit_chunks = len(data)//4

		datalines	= [None] * number_of_32_bit_chunks
		dataints 	= np.zeros(number_of_32_bit_chunks, dtype=np.int64)

		for i in range(number_of_32_bit_chunks):
			datalines[i]	= data[4*i:4*(i+1)]
			dataints[i] 	= int.from_bytes(datalines[i], byteorder='little')

		#seperate the first four bits (data is now in Most Significant Bit First).
		channels       	= np.zeros(number_of_32_bit_chunks, dtype=np.int32)
		quantized_times	= np.zeros(number_of_32_bit_chunks, dtype=np.int32)

		for i in range(number_of_32_bit_chunks):
			channels[i]       	= dataints[i] >> 30	
			quantized_times[i]	= (0xffFFffFF >> 2) & dataints[i]
			if verbose:
				print("0b{:02b}:{:030b}".format(channels[i],quantized_times[i]))

		return channels, quantized_times

	def decode_header(self, header, verbose=False):
		''' dictionary = decode_header(header)

		Takes the header datastream and splits it into keys and values in
		dictionary.

		All values are strings.

		'''

		dictionary = {}

		header = header.decode('utf-8')	#convert bytestream to string
		header = header.splitlines()   	#break up into line by line.

		#remove the datafile timestamp before extracting keys and values.
		dictionary['timestamp'] = header.pop()

		for line in header:
			if line[0] == ';':
				#skip commented lines.
				continue
			if '=' in line:
				split_line = line.split('=')
			else:
				split_line = line.split(':')

			#strip removes leading and trailing whitespace.
			dictionary[split_line[0]] = split_line[1].strip()

		if verbose:
			print(dictionary)
		
		return dictionary

	def unzip_data(self):
		pass

if __name__ == '__main__':
	''' Testbench for checking data extraction '''
	print("In Main:")

	worker = P7888_Worker()
	worker.transition_to_manual()
