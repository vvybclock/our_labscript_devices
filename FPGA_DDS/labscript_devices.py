import h5py
import numpy as np
from labscript import Device, set_passed_properties
# from math import floor

# A "labscript_device" is what one defines in the connection table. It's how
# labscript knows how to drive the device. Here we are defining an
# "unbuffered" device. Something that runs on its own CPU time, and  something
# we just need to send data to every so often. It's interface is not timing
# critical.

###########################################################################
#		Written by Chi Shu (chishu@mit.edu)	c. July 2021	
###########################################################################


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
		self.ClockRate = 480*10**6 
		# number of bits for frequency word
		self.freqbits = 32
		# number of bits for phase word
		self.phasbits = 14
		# 
		self.amplbits = 10 
		# commands is a list of channel, function, Data, Unit, RampRate (in unit of us)
		self.ts = []
		self.commands = []
		self.descriptions = []
		self.commands_human = []
		# self.constant(0.01, 1, 'freq', 80, 'MHz','initial value')
		# self.constant(0.2, 1, 'phas', 360, 'Degrees', 'set phase')
		# self.ramp(    0.5, 0.2, 1, 'freq', 80, 'MHz', 1,  'Hz', 1, 'Ramp to next value' )


	#labscript optional? commands here.

	def generate_code(self,hdf5_file):
		''' Simply saves the set point for the FPGA_DDS frequency in the HDF.
		'''
		grp 	= hdf5_file.require_group(f'/devices/{self.name}/')
		dset	= grp.require_dataset('ts',(1,),dtype='f')

		dset = self.ts

		print(self.ts)
		print(self.commands)
		print(self.descriptions)
		print(self.commands_human)
		
		

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
		elif (func == 1):
			data = round(Data*Units[unit]/360*2**self.phasbits)
		elif (func == 2):
			data = round(Data*2**self.amplbits)
		self.constant_raw(t,channel, func, data, description)
		self.commands_human.append([t, channel, Func, Data, unit, description])
		

	def constant_raw(self, t, channel, func, data, description = ''):
		'''  
		set constant setting to FPGA_DDS in raw AD9959 format

		'''
		last_index = len(self.ts)
		if(last_index == 0):
			self.addnewcommands(t, channel, func, data, 0, description)	
		elif(self.ts[last_index-1] < t):
			self.addnewcommands(t, channel, func, data, 0, description)
		else:
			raise ErrorValue("FPGA DDS timing conflicts"+description)
		
	def ramp(self, t, dt, channel, Func, Data, unit1, rampstep, unit2, ramprate, description = ''):
		us = 10**-6
		Funcs = {'freq':0, 'phas':1, 'ampl':2}
		Units = {'MHz': 1.0*10**6, 'kHz': 1.0*10**3, 'Hz': 1.0, 'mHz': 0.001,
		 'Degree': 1, 'Degrees':1, 'Rads': 180/(3.1415926), 'None':1, '1':1}
		NumofStep = round(dt/(us*ramprate))
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

		self.ramp_raw(t, channel, func, rampstep, ramprate, description+'_ramp_start')
		self.commands_human.append([t, dt, channel, Func, Data, unit1, rampstep, unit2, ramprate, description])
		self.constant_raw(t+(ramprate*NumofStep+1)*us, channel, func, data+rampstep*NumofStep, description+'_ramp_stop' )
		# self.commands_human.append([t, channel, Func, ])
		# self.constant(t+(ramprate*NumofStep+1)*us, channel, Func, Data+rampstep*NumofStep, unit, description+'_ramp_stop' )
		# return [t+(ramprate*NumofStep+1)*us, Data+rampstep*NumofStep]

	def ramp_raw(self, t, channel, func, rampstep, ramprate, description = ''):
		last_index = len(self.ts)
		if(last_index == 0):
			self.addnewcommands(t, channel, func, rampstep, ramprate, description)
		elif(self.ts[last_index-1] < t):
			self.addnewcommands(t, channel, func, rampstep, ramprate, description)
		else:
			raise ErrorValue("FPGA DDS timing conflicts"+description)

		
	def addnewcommands(self, t, channel, func, data, ramprate, description = ''):
		self.ts.append(t)
		self.commands.append([channel, func, data, ramprate])
		self.descriptions.append(description)