###########################################################################
#		Written by Enrique Mendez (eqm@mit.edu)	c. April 2021
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

FONT = "Helvetica"
FONTSIZE = 24
class FPGA_DDSTab(DeviceTab):
	
	def initialise_workers(self):
		#Does spelling of the function name matter? (-ize vs -ise?)

		#Look up Connection Settings from the Connection Table
		connection_table = self.settings['connection_table']
		device = connection_table.find_by_name(self.device_name)

		#pull particular settings needed here.
		# particular_setting = device.properties['particular_setting_identifier']
		usbport = device.properties['usbport']

		#Start the worker process associated with our worker class.
		#Pass it the particular settings it needs to connect.
		self.create_worker(
			'main_worker',
			'user_devices.FPGA_DDS.blacs_worker.FPGA_DDS_Worker',
			{'usbport' : usbport},
		)

		self.primary_worker = 'main_worker'

	def initialise_GUI(self):
		# self.get_channels()

		# channels = self.channels
		layout = self.get_tab_layout()
		self.label_widgets = {}
		
		self.label_widgets =  QLabel("test")
		self.label_widgets.setText(f'{1:20}:{0:5.02f} asdfa')
		self.label_widgets.setAlignment(Qt.AlignCenter)
		f = QFont(FONT, FONTSIZE)
		self.label_widgets.setFont(f)
		layout.addWidget(self.label_widgets)


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
		
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.update)
		# self.timer.start(100)
		pass

	def update(self):
		step = 480*10**6/2**32
		DDS_HEX = self.spinbox_widgets[0].value()/480/10**6*2**32//1
		# self.spinbox_widgets[0].setValue(step*DDS_HEX)
		self.spinbox_widgets[1].setValue(DDS_HEX)
		pass


	# def get_channels(self):
	#	#Look up Connection Settings from the Connection Table
	#	connection_table = self.settings['connection_table']
	#	device = connection_table.find_by_name(self.device_name)

	#	#pull particular settings needed here.
	#	self.channels = device.properties['channels']



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
