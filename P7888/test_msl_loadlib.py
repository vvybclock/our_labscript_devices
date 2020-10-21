
# IPC and MSL-Loadlib
#
# labscript is run on 64 bit python. the p7888 dll is written as a 32 bit
# application. To run the DLL we need to use 'inter process communication'.
# Something that will execute a 32 bit program to talk  to the 32 bit DLL and
# then act as an interface to our 64 bit labscript program. There is
# fortunately a python library that  does this. msl-loadlib.
#
# Installing MSL-Loadlib
#	Commands:
#		conda activate ybclock_v0_1                                  	#loads our virtual environment
#		conda install pip                                            	#installs pip into our virtual environment
#		.\Anaconda3\envs\ybclock_v0_1\Scripts\pip install msl-loadlib	#installs msl-loadlib into our virtual environment.
#		Successfully installed msl-loadlib-0.7.0
#
# Testing MSL-Loadlib
#
#	See: https://msl-loadlib.readthedocs.io/en/latest/interprocess_communication.html

#test_my_client.py

from msl.loadlib import Client64

class MyClient(Client64):
	""" Send a request to 'MyServer' to execute the 'add' method and get the response. """

	def __init__(self):
		# Specify the name of the python module to execute on the 32-bit server (i.e., 'my_server')
		super(MyClient,self).__init__(module32='test_my_server')

	def add(self,a,b):
		# The Client64 class has a 'request32' method to send a request to the 32-bit server.
		# Send the 'a' and 'b' arguments to the 'add' method in MyServer.
		return self.request32('add', a , b)

if __name__ == '__main__':
	my_client = MyClient()
	print(c.add(1,2))
