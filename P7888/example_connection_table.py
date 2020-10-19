#we need to define the device in the connection table. Why?!

from labscript import start, stop

#Because EVERY connection table must have a Pseudoclock
from labscript_device.DummyPseudoclock.labscript_devices import DummyPseudoclock

#Our Custom Device
from user_devices.P7888.labscript_devices import P7888

#Define the two devices with their own names and connection info
DummyPseudoclock('dummy_pseudoclock')
CustomArduinoDevice('arduino',com_port='COM1')

# AT THIS STAGE! We have only called the constructor to our Custom Device. To
# understand what it's doing we head to it's source code. Which is clearly
# defined from the import line.

# This constructor only really defines settings, and writes them to the HDF
# file. These settings are accessed later by "blacs_tabs" and "blacs_worker"
# functions which are recognized by the BLACS program via the register_classes.py
# script. See that file for more.
if __name__ == '__main__':
	start()
	stop(1)