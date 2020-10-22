import h5py

from labscript import Device, set_passed_properties


# A "labscript_device" is what one defines in the connection table. It's how
# labscript knows how to drive the device. Here we are defining an
# "unbuffered" device. Something that runs on its own CPU time, and  something
# we just need to pull data from every so often. It's interface is not timing
# critical.

#This "labscript_device"


class P7888(Device):
	"""A labscript device for periodically pulling data from the P7888 photon counter."""

	# Labscript REQUIRED Commands Here

	# This decorator declares that some keyword arguments should be saved to the
	# connection table, so that BLACS can read them:
	# The P7888 uses a DLL to communicate with the software that communicates
	# with the card. This DLL only needs the abstract specifier nDisplay (maybe
	# nDevices? nSystems?) to communicate with the appropriate card. So that is
	# the property we decide to save. See p7888_photon_counter.py for explicit
	# example usage.
	@set_passed_properties({'connection_table_properties': ['nDisplay', 'nSystem']})
	def __init__(self, name, nDisplay=0, nSystem=0): #redefine the class constructor
		#piggy back on working code for the class constructor
		Device.__init__(self, name=name, parent_device=None, connection=None)

		#add whatever else we need for the custom constructor i.e., class variables.
		self.custom_class_variable = []
		
		# The existence of this attribute is how BLACS knows it needs to make a tab for
		# this device:
		# STILL, HOW DOES BLACS KNOW WHERE TO FIND THE TAB CLASS????
		# It uses register_classes.py, which it's defined to scan for.
		self.BLACS_connection = nDisplay

	# Labscript OPTIONAL? Commands Here

	# generate_code runs when your shot is compiled by runmanager. No
	# communication with hardware should occur here. Of course, if you write code
	# here that communicates with hardware, it will run, but that is not the
	# intended role of this function. generate_code() should process any
	# instructions the user has added in their labscript code, converting them to
	# the low-level instructions that need to be programmed into the device, and
	# then save those instructions to the shot file. These instructions will
	# later be parsed by a BLACS_tab/worker function so it needs to be only
	# understandble by the program you will write.

	def generate_code(self, hdf5_file):
		pass

	# DEFINE USER COMMANDS HERE
	def custom_user_command(self, args):
		pass