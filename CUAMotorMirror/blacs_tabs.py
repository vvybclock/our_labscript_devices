###########################################################################
#		Written by Chi Shu (shu@g.harvard.edu)	c. Oct 2021
###########################################################################
#To see how this file is accessed by labscript see register_classes.py

from qtutils.qt.QtCore import *
from qtutils.qt.QtGui import *
from qtutils.qt.QtWidgets import *
from qtutils import UiLoader
from labscript_utils.qtwidgets.toolpalette import ToolPaletteGroup

from blacs.tab_base_classes import Tab, Worker, define_state
from blacs.tab_base_classes import MODE_MANUAL, MODE_TRANSITION_TO_BUFFERED, MODE_TRANSITION_TO_MANUAL, MODE_BUFFERED
from blacs.device_base_class import DeviceTab
import os
import serial.tools.list_ports

FONT = "Helvetica"
FONTSIZE = 24
DeviceFilepath = os.path.dirname(os.path.realpath(__file__))
class CUAMotorMirrorTab(DeviceTab):
	
	def initialise_workers(self):
		'''
		intialize worker with device properties
		'''
		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		# particular_setting = device.properties['particular_setting_identifier']
		usbport = device.properties['usbport']
		baud_rate = device.properties['baud_rate']
		self.usbport = usbport
		self._baud = baud_rate
		self.connected = False

		#Start the worker process associated with our worker class.
		#Pass it the particular settings it needs to connect.
		self.create_worker(
			'main_worker',
			'user_devices.CUAMotorMirror.blacs_worker.CUAMotorMirror_Worker',
			{'usbport' : usbport, 'baud_rate':baud_rate},
		)

		self.primary_worker = 'main_worker'


		# results = yield(self.queue_work(self.primary_worker, 'open_port', 1))
		# print(results)

	def initialise_GUI(self):
		# self.get_channels()

		# channels = self.channels
		layout = self.get_tab_layout()
		# self.label_widgets = {}
		
		# # self.label_widgets =  QLabel("test")
		# # self.label_widgets.setText(f'{1:20}:{0:5.02f} asdfa')
		# # self.label_widgets.setAlignment(Qt.AlignCenter)
		# # f = QFont(FONT, FONTSIZE)
		# # self.label_widgets.setFont(f)
		# # layout.addWidget(self.label_widgets)


		self.spinbox_widgets = {}
		for i in range(2):
			self.spinbox_widgets[i] = NoStealFocusDoubleSpinBox()
			self.spinbox_widgets[i].setDecimals(3)
			self.spinbox_widgets[i].setMaximum(2**32)
			layout.addWidget(self.spinbox_widgets[i])
		step = 480*10**6/2**32
		DDS_HEX = 80/480*2**32//1
		self.spinbox_widgets[0].setValue(step*DDS_HEX)
		self.spinbox_widgets[1].setValue(DDS_HEX)

		self.subWidget = UiLoader().load(os.path.join(DeviceFilepath, 'test.ui'))
		layout.addWidget(self.subWidget)
		# self.port_list_dropdown.
		self.text_lists = self.subWidget.Text_lists
		self.open_port_button = self.subWidget.Open_port_button
		self.open_port_button.pressed.connect(self.usbports_control)
		self.search_button = self.subWidget.search_button
		self.search_button.pressed.connect(self.search_motors)
		self.open_port()


		# self.text_lists.append('test')
		
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.update)
		# self.timer.start(100)

		# results = self.queue_work(self.primary_worker, 'open_port', 1)
		# print(results)
	
	def usbports_control(self):
		if self.open_port_button.text == 'Open Port':
			self.open_port()
		else:
			self.close_port()

	@define_state(MODE_MANUAL, queue_state_indefinitely = True)
	def close_port(self):
		'''
		close com port
		Not yet implemented
		'''
		self.open_port_button.setEnabled(False)
		results = yield(self.queue_work(self.primary_worker, 'close_port'))
		if results:
			self.connected = False
			
		pass


	@define_state(MODE_MANUAL, queue_state_indefinitely = True)
	def open_port(self):
		assert(self.connected == False)
		self.open_port_button.setEnabled(False)
		# read port list
		ports = serial.tools.list_ports.comports()
		portnamelist = [port for port, desc, hwid in sorted(ports)]
		portname = self.usbport
		if (portname in portnamelist) and (portname!=None):
			self.portname = portname
		else:
			# open pop dialog as user to select port
			PopDialog = UiLoader().load(os.path.join(DeviceFilepath, 'SelectPorts.ui'))
			self.PopDialog = PopDialog
			PopDialog.comboBox.clear()
			PopDialog.comboBox.addItems(portnamelist)
			PopDialog.show()
			returns = PopDialog.exec_()
			if returns == PopDialog.Accepted:
				self.portname = PopDialog.comboBox.currentText() 
			else:
				self.portname = None
		if self.portname != None:
			results = yield(self.queue_work(self.primary_worker, 'open_port', self.portname))
			if results:
				self.connected = True
				self.text_lists.append('True')
				self.open_port_button.setText("Close Port")
				self.open_port_button.setEnabled(True)
				pass
		else:
			pass
			#port open cancelled
	


	@define_state(MODE_MANUAL, queue_state_indefinitely = True)
	def search_motors(self):
		results = yield(self.queue_work(self.primary_worker, 'search_motors'))
		if results:
			self.text_lists.append(str(results))

	


class NoStealFocusDoubleSpinBox(QDoubleSpinBox):
    """A QDoubleSpinBox that doesn't steal focus as you scroll over it with a
    mouse wheel."""
    def __init__(self, *args, **kwargs):
        QDoubleSpinBox.__init__(self, *args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(Qt.WheelFocus)
        return QDoubleSpinBox.focusInEvent(self, event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        return QDoubleSpinBox.focusOutEvent(self, event)

    def wheelEvent(self, event):
        if self.hasFocus():
            return QDoubleSpinBox.wheelEvent(self, event)
        else:
            event.ignore()
