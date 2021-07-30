###############################################
# 
# /user_devices/FPGA_DDS/runviewer_parser.py     
# Copyright 2021  Chi Shu MIT
# This is the file display traces for FPGA_DDS
# Modify runviewer\_main_.py add_trace function add a line 
        # if con is None:
        #     return
# before con.device_class
# not sure how to implement it without change the original labscript codes
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
		with h5py.File(self.path, 'r') as f:
			instructions = f['/devices/'+self.name+'/Instructions']
			Time = instructions["Time"]
			Ch = instructions["Ch"]
			Func = instructions["Func"]
			RampRate = instructions["RampRate"]
			Data = instructions["Data"]
		try:
			print(Time)
			print(Ch)
			print(Func)
			print(RampRate)
			print(Data)
			Ch_freq = {}
			Ch_phase = {}
			Ch_amp = {}
			Numofsteps = len(Time)
			Ch_freqset = 0
			Ch_phaseset = 0
			Ch_ampset = 0
			# set initial condition
			Ch_freq[0]= [20]

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
			# check which channel has initial value, which don't Don't plot the lines without initial value
			time = [0]
			for i in range(Numofsteps):
				time.append(Time[i]/(100*10**6))
				for j in range(4):
					if 1<<j & Ch[i]:
						if RampRate[i] == 0:
							if Func[i] == 0:
								Ch_freq[j].append(Data[i]/2**self.freqbits*self.ClockRate)
								Ch_phase[j].append(Ch_phase[j][-1])
								Ch_amp[j].append(Ch_amp[j][-1])
							elif Func[i] == 1:
								Ch_freq[j].append(Ch_freq[j][-1])
								Ch_phase[j].append(Data[i]/2**self.phasbits*360)
								Ch_amp[j].append(Ch_amp[j][-1])
							elif Func[i] == 2:
								Ch_freq[j].append(Ch_freq[j][-1])
								Ch_phase[j].append(Ch_phase[j][-1])
								Ch_amp[j].append(Data[i]/2**self.amplbits)
					else:
						Ch_freq[j].append(Ch_freq[j][-1])
						Ch_phase[j].append(Ch_phase[j][-1])
						Ch_amp[j].append(Ch_amp[j][-1])


			print(time)
			print(Ch_freq[0])
			print(Ch_phase)
			print(Ch_amp)



			
			add_trace(self.name+'/Ch0/freq',(time,Ch_freq[0]), self.name, 'test2')
			add_trace(self.name+'/Ch1/freq',(time,Ch_freq[1]), self.name, 'test2')
			add_trace(self.name+'/Ch2/freq',(time,Ch_freq[2]), self.name, 'test2')
			add_trace(self.name+'/Ch3/freq',(time,Ch_freq[3]), self.name, 'test2')
		except Exception as e:
			print(e)
			# sys.stdout = sys.__stdout__
		else:
			pass
		finally:
			pass	
		# This device don't trigger any other devices
		trigger = {}
		return trigger

    



