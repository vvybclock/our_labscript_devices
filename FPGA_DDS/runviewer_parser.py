###############################################
# 
# /user_devices/FPGA_DDS/runviewer_parser.py     
# Copyright 2021  Chi Shu MIT
# This is the file display traces for FPGA_DDS
# Latest update:
# No need to modify runviwer\_main_.py file. 
# library inspect read back the instance of class shot in _main_.py and overwrite add_trace function.
###############################################


from labscript_devices import runviewer_parser 
from labscript import LabscriptError
import h5py
import numpy as np
    
@runviewer_parser
class FPGA_DDSParser(object):
	def __init__(self, path, device):
		self.path = path
		self.name = device.name
		self.device = device
		self.ClockRate = 480*10**6 
		# number of bits for frequency word
		self.freqbits = 32
		# number of bits for phase word
		self.phasbits = 14
		# 
		self.amplbits = 10 


	def get_traces(self, add_trace, clock = None):
		# read back calling instance of class shot
		import inspect 
		shot = inspect.currentframe().f_back.f_locals['self']
		# overwrite add_trace function in runviwer/_main_.py to accomodate no device_class attribute of con
		def add_trace_overwrite(shot, name, trace, parent_device_name, connection):
			name = str(name)
			shot._channels[name] = {'device_name': parent_device_name, 'port': connection}
			shot._traces[name] = trace
			# add shutter times
			con = shot.connection_table.find_by_name(name)
		# read from h5py file
		with h5py.File(self.path, 'r') as f:
			instructions = f['/devices/'+self.name+'/Instructions']
			Time = instructions["Time"]
			Ch = instructions["Ch"]
			Func = instructions["Func"]
			RampRate = instructions["RampRate"]
			Data = instructions["Data"]
		try:
			# print(Time)
			# print(Ch)
			# print(Func)
			# print(RampRate)
			# print(Data)
			# channel settings Ch_freq[0] is the ch0 frequency
			Ch_freq = {}
			Ch_phase = {}
			Ch_amp = {}
			Ch_time = {}
			Numofsteps = len(Time)
			# 4bit binary word to store channels initialzed.
			Ch_freqset = 0
			Ch_phaseset = 0
			Ch_ampset = 0
			# set initial condition
			Ch_freq[0]= []
			# scan through to set initial value of freq, phase and amp by the first constant setting.
			# set ch_freqset's correspoinding bit to 1 when first constant setting is found
			for i in range(Numofsteps):
				for j in range(4):
					if 1<<j & Ch[i]:
						if RampRate[i] == 0:
							if Func[i] == 0:
								# freq
								if Ch_freqset & 1<<j:
									pass
								else:
									Ch_freq[j] = [Data[i]/(2**self.freqbits)*self.ClockRate]
									# set initial frequency value
									Ch_freqset+= 1<<j
									# set flag for Ch0 frequency initial set
							elif Func[i] == 1:
								# phase
								if Ch_phaseset & 1<<j:
									pass
								else: 
									Ch_phase[j] = [Data[i]/(2**self.phasbits)*360]
									# set initial phase value
									Ch_phaseset+= 1<<j
									# set flag for Ch0 phase initial set
							elif Func[i] == 2:
								# amp
								if Ch_ampset & 1<<j:
									pass
								else:
									Ch_amp[j] = [Data[i]/(2**self.amplbits)]
									# set initial phase value
									Ch_ampset+= 1<<j
									# set flag for Ch0 amp initial set	
						else:
							if (Func[i] == 0) and not (Ch_freqset & 1<<j):
								Ch_freq[j] = [-10**6]
							elif (Func[i] == 1) and not (Ch_phaseset & 1<<j):
								Ch_phase[j] = [-10**6]
							elif (Func[i] == 2) and not (Ch_ampset & 1<<j):
								Ch_amp[j] = [-10**6]
				if Ch_freqset == 15 and Ch_phaseset ==15 and Ch_ampset == 15:
					break
			# find channels without initial value. Set -10**6 to channels has no initial value
			for j in range(4):
				# set initial time stamps
				Ch_time[j] = [0]
				if not (1<<j & Ch_freqset):
					Ch_freq[j] = [-10**6]
				if not (1<<j & Ch_phaseset):
					Ch_phase[j] = [-10**6]
				if not (1<<j & Ch_ampset):
					Ch_amp[j] = [-10**6]  
			# scan through tables to set constant and ramp
			for i in range(Numofsteps):
				# time.append(Time[i]/(100*10**6))
				for j in range(4):
					if 1<<j & Ch[i]:
						if RampRate[i] == 0:
							if Func[i] == 0:
								Ch_time[j].append(Time[i]/(100*10**6))
								Ch_freq[j].append(Data[i]/2**self.freqbits*self.ClockRate)
								Ch_phase[j].append(Ch_phase[j][-1])
								Ch_amp[j].append(Ch_amp[j][-1])
							elif Func[i] == 1:
								Ch_time[j].append(Time[i]/(100*10**6))
								Ch_freq[j].append(Ch_freq[j][-1])
								Ch_phase[j].append(Data[i]/2**self.phasbits*360)
								Ch_amp[j].append(Ch_amp[j][-1])
							elif Func[i] == 2:
								Ch_time[j].append(Time[i]/(100*10**6))
								Ch_freq[j].append(Ch_freq[j][-1])
								Ch_phase[j].append(Ch_phase[j][-1])
								Ch_amp[j].append(Data[i]/2**self.amplbits)
						else:
							# ramp
							if i == Numofsteps-1 or i == 0:
								LabscriptError("First and last entry can't be ramp") 
							else:
								NumofRampStep = round((Time[i+1]-Time[i])/100/RampRate[i])
								counter = 0
								Ch_freq_last = Ch_freq[j][-1]
								Ch_phase_last = Ch_phase[j][-1]
								Ch_amp_last = Ch_amp[j][-1]
								for k in range(NumofRampStep):
									counter += 1
									Ch_time[j].append((Time[i]/100+counter*RampRate[i])/10**6)
									if Func[i] == 0:
										Ch_phase[j].append(Ch_phase[j][-1])
										Ch_amp[j].append(Ch_amp[j][-1])
										if Data[i] <= 2**31:
											Ch_freq[j].append(Ch_freq_last+(counter*Data[i])/2**self.freqbits*self.ClockRate)
										else:
											Ch_freq[j].append(Ch_freq_last+(counter*(Data[i]-2**32))/2**self.freqbits*self.ClockRate)
									elif Func[i] == 1:
										Ch_freq[j].append(Ch_freq[j][-1])
										Ch_amp[j].append(Ch_amp[j][-1])
										if Data[i] <= 2**31:
											Ch_phase[j].append(Ch_phase_last+(counter*Data[i])/2**self.phasbits*360)
										else:
											Ch_phase[j].append(Ch_phase_last+(counter*(Data[i]-2**32))/2**self.phasbits*360)				
									elif Func[i] == 2:
										Ch_freq[j].append(Ch_freq[j][-1])
										Ch_phase[j].append(Ch_phase[j][-1])
										if Data[i] <= 2**31:
											Ch_amp[j].append(Ch_amp_last+(counter*Data[i])/2**self.amplbits)
										else:
											Ch_amp[j].append(Ch_amp_last+(counter*(Data[i]-2**32))/2**self.amplbits)
					else:
						pass


			# print(Ch_freq)
			# print(Ch_phase)
			# print(Ch_amp)



			for j in range(4):
				if (Ch_freq[j][0]>=0):
					add_trace_overwrite(shot, f"{self.name}/Ch{j}/freq",(Ch_time[j],Ch_freq[j]), self.name, '')
				if (Ch_phase[j][0]>=0):
					add_trace_overwrite(shot, f"{self.name}/Ch{j}/phase",(Ch_time[j],Ch_phase[j]), self.name, '')
				if (Ch_amp[j][0]>=0):
					add_trace_overwrite(shot, f"{self.name}/Ch{j}/amp", (Ch_time[j], Ch_amp[j]), self.name, '')
			
		except Exception as e:
			# print(e)
			sys.stdout = sys.__stdout__
		else:
			pass
		finally:
			pass	
		# This device don't trigger any other devices
		trigger = {}
		return trigger

    



