from msl.loadlib import Server32

class MyServer(Server32):
	""" A wrapper around a 32-bit C++ library, 'cpp_lib32.dll', that has an 'add' function."""

	def __init__(self, host, port, quiet, **kwargs):
		# Load the 'cpp_lib32' shared-library file using ctypes.CDLL
		library_dir = r'C:\Users\Boris\anaconda3\envs\ybclock_v0_1\Lib\site-packages\msl\examples\loadlib'
		lib_loc = library_dir + '\\' + r'cpp_lib32.dll'
		super(MyServer, self).__init__(lib_loc, 'cdll', host, port, quiet)

	def add(self,a, b):
		# The Server32 class has a 'lib' property that is a reference to the ctypes.CDLL object.
		# The shared library's 'add' function takes two integers as inputs and returns the sum
		return self.lib.add(a,b)
