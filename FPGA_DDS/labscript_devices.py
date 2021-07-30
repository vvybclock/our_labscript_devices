import h5py
import numpy as np
from labscript import TriggerableDevice, set_passed_properties, config, LabscriptError
# from math import floor

# A "labscript_device" is what one defines in the connection table. It's how
# labscript knows how to drive the device. Here we are defining an
# "unbuffered" device. Something that runs on its own CPU time, and  something
# we just need to send data to every so often. It's interface is not timing
# critical.

###########################################################################
#		Written by Chi Shu (chishu@mit.edu)	c. July 2021	
###########################################################################


class FPGA_DDS(TriggerableDevice):
	''' A labscript device for sending frequency setpoints. '''

	frequency_MHz = None

	# Labscript REQUIRED Commands Here

	# This decorator declares that some keyword arguments should be saved to the
	# connection table, so that BLACS can read them:
	@set_passed_properties({'connection_table_properties' : ['usbport']})
	def __init__(self, name, parent_device, usbport, connection):

		TriggerableDevice.__init__(self, name=name, parent_device = parent_device, connection=connection)

		# The existence of this attribute is how BLACS knows it needs to make a tab for
		# this device:
		# STILL, HOW DOES BLACS KNOW WHERE TO FIND THE TAB CLASS????
		# It uses register_classes.py, which it's defined to scan for.
		self.BLACS_connection = usbport
		self.t00 = 1*10**(-3)
		self.t00 = round(self.t00,10)
		self.ClockRate = 480*10**6 
		# number of bits for frequency word
		self.freqbits = 32
		# number of bits for phase word
		self.phasbits = 14
		# 
		self.amplbits = 10 
		# commands is a list of channel, function, Data, Unit, RampRate (in unit of us)
		self.instructions = {}
		self.ramp_limits = []
		self.commands_human = []
		# self.constant(0.01, 1, 'freq', 80, 'MHz','initial value')
		# self.constant(0.2, 1, 'phas', 360, 'Degrees', 'set phase')
		# self.ramp(    0.5, 0.2, 1, 'freq', 80, 'MHz', 1,  'Hz', 1, 'Ramp to next value' )


	#labscript optional? commands here.

	def generate_code(self,hdf5_file):
		''' Parse commands and timings and save the correct sequence into HDF file.
		'''


		grp	= hdf5_file.require_group(f'/devices/{self.name}/')
		
		# sort in time and create table to save
		times = sorted(list(self.instructions.keys()))
		FPGA_table_keys = ['Time', 'Ch', 'Func', 'RampRate', 'Data']
		dtypes = [(c, np.uint32) for c in FPGA_table_keys]
		dtypes.append(('Description', 'S50'))
		# dtypes.append(('Description', object))
		FPGA_Commands_table = np.empty(len(times), dtype = dtypes)
		for index in range(len(times)):
			time = times[index]
			FPGA_Commands_table[index] = (time*100*10**6, self.instructions[time]['Ch'], 
						self.instructions[time]['Func'] , self.instructions[time]['RampRate'] ,
						self.instructions[time]['Data'] , self.instructions[time]['Description'])

		# save to HDF file
		grp.create_dataset('Instructions', data = FPGA_Commands_table, compression = config.compression)	
		
		# print("Human commands")
		# print(self.commands_human)
		# print("Instructions:")
		# print(self.instructions)

	def add_instruction(self, time, instruction = None):
		# round time to 0.1 ns to revent floating points
		time = round(time, 10)
        # Check that time is not negative or too soon after t0:
		if time < self.t00:
			err = ' '.join([self.description, self.name, 'has an instruction at t=%ss,'%str(time),
				'Due to the delay in triggering its pseudoclock device, the earliest output possible is at t=%s.'%str(self.t0)])
			raise LabscriptError(err)
        # Check that this doesn't collide with previous instructions:
		if time in self.instructions.keys():
			if not config.suppress_all_warnings:
				message = ' '.join(['WARNING: State of', self.description, self.name, 'at t=%ss'%str(time),
                          'has already been set to %s.'%self.instruction_to_string(self.instructions[time]),
                          'Overwriting to %s. (note: all values in base units where relevant)'%self.instruction_to_string(self.apply_calibration(instruction,units) if units and not isinstance(instruction,dict) else instruction)])
				sys.stderr.write(message+'\n')
		
		self.instructions[time] = instruction
            
	def triggerSet(self, t00):
		# set t0 for the trigger
		self.t00 = round(t00, 10)

	def constant(self, t, channel=0, Func= 'freq', Data = 0, unit = 'None', description = ''):
		'''  
		set frequency to constant for FPGA_DDS at time t, with channel and Function
		channel is defined as 4 bit, b'0001' means channel 0, b'0011' means both channel 0 and 1 ...
		Func: 'freq', 'phas', 'ampl'
		Data: Value to be set, either frequency as kHz (0-480MHz), phase as degree (0-360), amplitude (0-1)

		'''
		Funcs = {'freq': 0, 'frequency':0, 'phas': 1, 'phase':1, 'ampl': 2, 'amplitude':2}
		Units = {'MHz': 1.0*10**6, 'kHz': 1.0*10**3, 'Hz': 1.0, 'mHz': 0.001,
		 'Degree': 1, 'Degrees':1, 'Rads': 180/(3.1415926), 'None':1, '1':1}
		func = Funcs[Func]
		if (func == 0):
			data = round(Data*Units[unit]/self.ClockRate*2**self.freqbits)
			data = data & 0xffffffff
		elif (func == 1):
			Data = Data*Units[unit]
			Data = Data % 360
			data = round(Data/360*2**self.phasbits)
			data = data & 0x00003fff
		elif (func == 2):
			Data = Data % 1
			data = round(Data*2**self.amplbits)
		self.commands_human.append({'Time':t, 'Ch': channel, 'Func': Func, 'Data': Data,
								 'Unit':unit, 'Description': description})
		self.add_instruction(t, {'Ch': channel, 'Func': func, 'RampRate': 0, 'Data': data,'Description': description})
		
	def ramp(self, t, dt, channel, Func, Data, unit1, rampstep, unit2, ramprate, description = ''):
		# ramp rate is in unit of 1us
		us = 10**-6
		# Ramprate is an integer
		ramprate = round(ramprate)
		Funcs = {'freq':0, 'phas':1, 'ampl':2}
		Units = {'MHz': 1.0*10**6, 'kHz': 1.0*10**3, 'Hz': 1.0, 'mHz': 0.001,
		 'Degree': 1, 'Degrees':1, 'Rads': 180/(3.1415926), 'None':1, '1':1}
		if dt < 0:
			err = 'Timing conflict FPGA DDS'.join([self.name, 'from t = %ss to %ss'%(str(t),str(endtime))])
			raise LabscriptError(err)
		# Round start and stop time to 0.1 ns
		t = round(t, 10)
		endtime = round(t+dt, 10)
		dt = endtime - t
		NumofStep = round(dt/(us*ramprate))
		endtime = t + (ramprate*NumofStep)*us
		dt = endtime-t

		for start, end in self.ramp_limits:
			if start < t < end or start < endtime < end:
				err = 'Timing conflict FPGA DDS'.join([self.name, 'from t = %ss to %ss'%(str(t),str(endtime))])
				raise LabscriptError(err)
		self.ramp_limits.append(([t, endtime]))
		# Convert from human value to device value
		func = Funcs[Func]
		if(func == 0):
			data = round(Data*Units[unit1]/self.ClockRate*2**self.freqbits)
			rampstep = round(rampstep*Units[unit2]/(self.ClockRate/2**self.freqbits))
		elif (func == 1):
			data = round(Data*Units[unit1]/360*2**self.phasbits)
			rampstep = round(rampstep*Units[unit2]/360*2**self.phasbits)
		elif (func ==2):
			data = round(Data*2**self.amplbits)
			rampstep = round(rampstep*2**self.amplbits)
		self.add_instruction(t, {'Ch': channel, 'Func': func, 'Data': rampstep, 
				'RampRate': ramprate, 'Description': description+'_ramp_start'})
		self.add_instruction(endtime, {'Ch': channel, 'Func': func,  
				'RampRate': 0, 'Data': data+rampstep*NumofStep, 'Description': description+'_ramp_end'})
		self.commands_human.append([t, dt, channel, Func, Data, unit1, rampstep, unit2, ramprate, description])
		return dt
