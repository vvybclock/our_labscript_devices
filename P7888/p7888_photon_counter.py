###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2020	
###########################################################################

import user_devices.P7888.p7888_dll

def is_started(nDisplay=0):
	status = p7888_dll.ACQSTATUS()
	p7888_dll.GetStatusData(status,nDisplay)
	is_started = status.started
	return bool(is_started)

def get_and_print_number_of_cards():
	print("###### Card Quantity Information")
	print()
	struct = p7888_dll.ACQDEF()
	print("Number of Modules : {}".format(struct.nDevices))
	print("Number of Active Displays : {}".format(struct.nDisplays))
	print("Number of Systems : {}".format(struct.nSystems))
	print("Controlled by MCDWIN? : {}".format(bool(struct.bRemote == 1)))

def get_and_print_settings(nDisplay=0):

	print("###### Device Settings for nDisplay = {}".format(nDisplay))
	print()

	settings = p7888_dll.ACQSETTING()

	p7888_dll.GetSettingData(settings, nDisplay)

	#print range
	print("Spectrum Length - 'range' : {}".format(settings.range))
	print()
	
	#print prena
	print("Enabled Presets:")
	prena_val = settings.prena
	setting = [
		"Realtime Preset Enabled", 
		"Single Sweeps Enabled",
		"Sweep Preset Enabled",
		"ROI Preset Enabled",
		"Starts Preset Enabled",
		"ROI2 Preset Enabled",
		"ROI3 Preset Enabled",
		"ROI4 Preset Enabled"
		]
	for bit in range(0,8):
		value = (prena_val & (1 << bit))
		print("\t{} : {}".format(setting[bit], bool(value)))
	print()

	#print ssweeps
	print("Number of Sweeps for Single Sweep Mode : {}".format(settings.ssweeps))

	#print roimin
	print("Lower ROI Limit : {}".format(settings.roimin))

	#print roimax
	print("Upper ROI Limit : {}".format(settings.roimax))

	#print eventpreset
	print("ROI Preset Value : {}".format(settings.eventpreset))

	#print timepreset
	print("Time Preset Value : {}".format(settings.timepreset))

	#print savedata
	print()
	print("Save Data Mode:")
	savedata_val = settings.savedata
	setting = [
		"Auto Save After Stop",
		"Write List File",
		"Listfile Only, No Histogram"
		]
	for bit in range(0,3):
		value = (savedata_val & (1 << bit))
		print("\t{} : {}".format(setting[bit], bool(value)))
	print()

	#print fmt
	setting = ["ASCII", "Binary"]
	print("Data Format : {}".format(setting[settings.fmt]))

	#print autoinc
	print("Auto Increment Filename? : {}".format(bool(settings.autoinc == 1)))

	#print cycles
	print("Cycles for Sequential Mode : {}".format(settings.cycles))

	#print sweepmode
	print("Sweepmode Bits : {}".format(hex(settings.sweepmode)))

	#print syncout
	print("Sync Out? : {}".format(bool(settings.syncout)))

	#print bitshift
	print("Bitshift : {}".format(settings.bitshift))

	#print digval
	print("Digval : {}".format(settings.digval))

	#print digio
	print("Digio : {}".format(settings.digio))

	#print dac01
	print("Dac01 : {}".format(hex(settings.dac01)))

	#print dac23
	print("Dac23 : {}".format(hex(settings.dac23)))

	#print swpreset
	print("Sweep Preset Value : {}".format(settings.swpreset))

	#print nregions
	print("Number of regions : {}".format(settings.nregions))

	#print caluse
	print("Calibration Used? : {}".format(bool(settings.caluse & 1)))
	print("Calibration 'formula' : {}".format(hex(settings.caluse >> 1)))

	#print fstchan
	print("First Time Channel in 16 ns units : {}".format(settings.fstchan))

	#print active
	print("Is module enabled in system 1? : {}".format(bool(settings.active == 1)))

	#print calpoints
	print("Number of Calibration Points : {}".format(settings.calpoints))

def set_to_sweep_mode(nDisplay=0):
	''' Sets the P7888 settings to sweep mode. 
	See the p7888_c_definitions for details. Or 
	the p7888 manual

	We want to collect as many sweeps as come in 
	without halting. This prevents a slow down in 
	data acquisition rate. Supposedly there's a 2
	second slow down when halting. Thus lowest four bits
	of sweepmode[0:3] are 0.

	The DMA bit in sweepmode[5] sets the card for high 
	counting rates if 1. See the manual 5.1.4 for more
	info on DMA mode.

	We assume no wraparound is needed. This is the case 
	when photons come in no later than 2s after the 
	start pulse. So sweepmode[6] = 0.

	I believe start event generation logs the start 
	events in the data file. This is useful for us
	as our start events will be periodically created
	by us.

	sweepmode[12] enables the 4 channel mode if the first bit is 
	zero.
	'''

	settings = p7888_dll.ACQSETTING()

	#set the data format to binary mode
	settings.fmt = 1 

	#disable all presets
	settings.prena = 0

	#enable sweep mode as described above.
	settings.sweepmode = 0x10A0

	#autoincrement file name?
	settings.autoinc = 0

	#dont send out synchronization pulses
	settings.syncout = 0

	#write to listfile continuously?
	settings.savedata = 0b010

	#use calibration
	settings.caluse = 1




	#write to list
	#i dont understand this. 
	#transfered from old settings
	settings.dac01 = 0x06660948
	settings.dac23 = 0x075c0666
	settings.digio = 0
	settings.digval = 0
	settings.fstchan = 0
	settings.bitshift = 0
	settings.range = 496000
	settings.roimax = 4096
	settings.timepreset = 1000.0
	settings.cycles = 1
	settings.active = 1
	settings.calpoints = 0

	#write_settings
	p7888_dll.StoreSettingData(settings, nDisplay)



if __name__ == '__main__':
	get_and_print_number_of_cards()
	get_and_print_settings()
	#set_to_sweep_mode()
	print("Started? : {}".format(is_started(nDisplay=0)))