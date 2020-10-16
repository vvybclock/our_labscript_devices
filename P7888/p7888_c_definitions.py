###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################

from ctypes import c_int, c_double, c_ulong, c_long, c_ubyte, c_uint, c_char
from ctypes import Structure, POINTER
from ctypes.wintypes import HANDLE

class ACQSTATUS(Structure):
	_fields_ = [
		("started", 	c_int),   	# acquisition status: 1 if running, 0 else
		("runtime", 	c_double),	# running time in seconds
		("totalsum",	c_double),	# total events
		("roisum",  	c_double),	# events within ROI
		("roirate", 	c_double),	# acquired ROI-events per second
		("nettosum",	c_double),	# ROI sum with background substracted
		("sweeps",  	c_double),	# Number of sweeps
		("stevents",	c_double),	# Start Events
		("maxval",  	c_ulong)  	# Maximum value in spectrum
	]

class ACQSETTING(Structure):
	_fields_ = [
		("range",      	c_ulong), 	# spectrum length
		("prena",      	c_long),  	# bit 0: realtime preset enabled
		               	          	# bit 1: single sweeps enabled
		               	          	# bit 2: sweep preset enabled
		               	          	# bit 3: ROI preset enabled
		               	          	# bit 4: Starts preset enabled
		               	          	# bit 5: ROI2 preset enabled
		               	          	# bit 6: ROI3 preset enabled
		               	          	# bit 7: ROI4 preset enabled
		("ssweeps",    	c_long),  	# number of single sweeps for single sweep mode
		("roimin",     	c_ulong), 	# lower ROI limit
		("roimax",     	c_ulong), 	# upper limit: roimin <= channel < roimax
		("eventpreset",	c_double),	# ROI preset value
		("timepreset", 	c_double),	# time preset value
		("savedata",   	c_long),  	# bit 0: 1 if auto save after stop
		               	          	# bit 1: write listfile
		               	          	# bit 2: listfile only, no histogram
		("fmt",        	c_long),  	# format type: 0 == ASCII, 1 == binary
		("autoinc",    	c_long),  	# 1 if auto increment filename
		("cycles",     	c_long),  	# for sequential mode
		("sweepmode",  	c_long),  	# sweepmode & 0xF:
		               	          	# 0 = normal, 4=sequential
		               	          	# bit 4: Softw. Start
		               	          	# bit 6: Wrap around
		               	          	# bit 5: DMA mode
		               	          	# bit 7: Start event generation
		               	          	# bit 12: 4 channel mode
		("syncout",    	c_long),  	# sync out bit 0..5 NIM syncout,
		               	          	# bit 6..12 TTL syncout
		               	          	# 0=OFF, 1=FIRST, 2=LAST, 3=FIFO1_FULL, 4=FIFO2_FULL,
		               	          	# 5=COUNT[0],...,31=COUNT[26],
		               	          	# 32...63=SWEEP[0]..SWEEP[31]
		("bitshift",   	c_long),  	# Binwidth = 2 ^ (bitshift)
		("digval",     	c_long),  	# digval=0..255 value for samplechanger
		("digio",      	c_long),  	# Use of Dig I/O, GO Line:
		               	          	# bit 0: status dig 0..3
		               	          	# bit 1: Output digval and
		               	          	# increment digval after stop
		               	          	# bit 2: Invert polarity
		               	          	# bit 3: Push-Pull output
		               	          	# bit 4..7: Input pins 4..7
		               	          	# Trigger System 1..4
		               	          	# bit 8: GOWATCH
		               	          	# bit 9: GO High at Start
		               	          	# bit 10: GO Low at Stop
		               	          	# bit 11: Clear before
		               	          	# ext. triggered Start
		("dac01",      	c_long),  	# LOWORD: DAC0 value (START)
		               	          	# HIWORD: DAC1 value (STOP 1)
		("dac23",      	c_long),  	# LOWORD: DAC2 value (STOP 2),
		               	          	# HIWORD: DAC3 value (STOP 3,4)
		("swpreset",   	c_double),	# sweep preset value
		("nregions",   	c_long),  	# number of regions
		("caluse",     	c_long),  	# bit 0 == 1 if calibration used,
		               	          	# higher bits: formula
		("fstchan",    	c_double),	# first time channel in 16 ns units
		("active",     	c_long),  	# 1 for module enabled in system 1
		("calpoints",  	c_long)   	# number of calibration points

	]

class ACQDATA(Structure):
	_fields_ = [
		("s0",      	POINTER(c_ulong)), 	# pointer to spectrum
		("region",  	POINTER(c_ulong)), 	# pointer to regions
		("comment0",	POINTER(c_ubyte)), 	# pointer to strings (c_ubyte == unsigned char)
		("cnt",     	POINTER(c_double)),	# pointer to counters
		("hs0",     	HANDLE),
		("hrg",     	HANDLE),
		("hcm",     	HANDLE),
		("hct",     	HANDLE)
	]

class ACQDEF(Structure):
	_fields_ = [
		("nDevices", 	c_int),	# Number of spectra = number of modules
		("nDisplays",	c_int),	# Number of active displays 0...nDevices
		("nSystems", 	c_int),	# Number of systems 0...4
		("bRemote",  	c_int),	# 1 if server controlled by MCDWIN
		("sys",      	c_uint)	# System definition word:
		             	       	# bit0=0, bit1=0: MCD#0 in system 1
		             	       	# bit0=1, bit1=0: MCD#0 in system 2
		             	       	# bit0=0, bit1=1: MCD#0 in system 3
		             	       	# bit0=1, bit1=1: MCD#0 in system 4
		             	       	# bit2=0, bit3=0: MCD#1 in system 1 ...
		             	       	# bit6=1, bit7=1: MCD#3 in system 4
	]
