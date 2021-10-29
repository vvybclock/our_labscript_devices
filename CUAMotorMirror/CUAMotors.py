############################################
#     Chi Shu (chishu@mit.edu) Oct-2021
############################################

# class of motors and mirrors

class CUAMotor(object):
	def __init__(self, device, ID):
		self._device = device
		self._ID = ID
		self.position = None
		self.load = None
		self.torque = False

		# read status

		pass

	def updateFull(self):
		pass

	def updateCore(self):
		pass

	def setTorque(self, status):
		pass

	def setTarget(self, target):
		pass
