from msl.loadlib import Client64, IS_PYTHON_64BIT

class MyClient(Client64):
	""" Send a request to 'MyServer' to execute the 'add' method and get the response. """

	def __init__(self):
		# Specify the name of the python module to execute on the 32-bit server (i.e., 'my_server')
		super(MyClient,self).__init__(module32='userlib.labscript_devices.P7888.p7888_server32')

	def __getattr__(self, method32):
		def send(*args, **kwargs):
			return self.request32(method32, *args, **kwargs)
		return send

if __name__ == '__main__':
	print("Is Python 64 bit?: {}".format(IS_PYTHON_64BIT))

	print("Starting Client...")
	my_client = MyClient()