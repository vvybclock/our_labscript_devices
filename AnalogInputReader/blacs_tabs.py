###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. 2021	
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

from qtutils.qt.QtCore import*
from qtutils.qt.QtGui import *
from qtutils.qt.QtWidgets import *

from blacs.tab_base_classes import Tab, Worker, define_state
from blacs.tab_base_classes import MODE_MANUAL, MODE_TRANSITION_TO_BUFFERED, MODE_TRANSITION_TO_MANUAL, MODE_BUFFERED
from blacs.device_base_class import DeviceTab

FONT = "Helvetica"
FONTSIZE = 24
class AnalogInputReaderTab(DeviceTab):
	
	def initialise_workers(self):
		#Does spelling of the function name matter? (-ize vs -ise?)

		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		# particular_setting = device.properties['particular_setting_identifier']
		channels = device.properties['channels']

		#Start the worker process associated with our worker class.
		#Pass it the particular settings it needs to connect.
		self.create_worker(
			'main_worker',
			'user_devices.AnalogInputReader.blacs_worker.AnalogInputReader_Worker',
			{'channels' : channels},
		)

		self.primary_worker = 'main_worker'

	def initialise_GUI(self):
		self.get_channels()

		layout = self.get_tab_layout()
		channels = self.channels
		self.label_widgets = {}
		for channel in channels:
			self.label_widgets[channel] = QLabel("test")
			self.label_widgets[channel].setText(f'{channel:20}:{0:5.02f} V')
			self.label_widgets[channel].setAlignment(Qt.AlignCenter)
			f = QFont(FONT, FONTSIZE)
			self.label_widgets[channel].setFont(f)
			layout.addWidget(self.label_widgets[channel])

		# add a timer for updating values
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(100)
		pass

	@define_state(MODE_MANUAL, queue_state_indefinitely=True, delete_stale_states=True)
	def update(self):
		self.get_channels()

		channels = self.channels
		for channel in channels:
			try:
				value = self.get_value(channels[channel])
				self.label_widgets[channel].setText(f'{channel:<20}:{value:03.03f} V')
			except:
				self.label_widgets[channel].setText(f'{channel:<20}: Error')

				pass

	def get_value(self, channel_name):
		import nidaqmx
		with nidaqmx.Task() as task:
			task.ai_channels.add_ai_voltage_chan(channel_name)
			value = task.read()
		return value

	def get_channels(self):
		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		self.channels = device.properties['channels']
