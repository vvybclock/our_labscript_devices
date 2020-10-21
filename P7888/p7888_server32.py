# A file that defines the 32 bit server that interfaces with the 32 bit P7888.DLL

import ctypes
from msl.loadlib import Server32
from p7888_c_definitions import *

class MyServer(Server32):
	""" A wrapper around the 32 bit P7888 photon counting card library. See p7888_dll.py"""

	def __init__(self, host, port, quiet, **kwargs):
		#Load the 'p7888_dll' using ctypes.WINDLL
		super(MyServer, self).__init__('C:/Windows/SysWOW64/DP7888.DLL', 'windll', host, port, quiet)

	def GetSettingData(self, nDisplay=0):
		settings = ACQSETTING()
		self.lib.GetSettingData(ctypes.pointer(settings), nDisplay)
		return settings

