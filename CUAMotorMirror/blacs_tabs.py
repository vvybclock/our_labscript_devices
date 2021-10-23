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
		self.open_port_button.pressed.connect(self.open_port)

		# self.text_lists.append('test')
		
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.update)
		# self.timer.start(100)

		# results = self.queue_work(self.primary_worker, 'open_port', 1)
		# print(results)
	@define_state(MODE_MANUAL, queue_state_indefinitely = True)
	def open_port(self):
		self.text_lists.append('read all ports')
		PopDialog = UiLoader().load(os.path.join(DeviceFilepath, 'SelectPorts.ui'))
		port_lists = yield(self.queue_work(self.primary_worker,'port_lists'))
		if port_lists:
			portsnamelist = [resourceinfo.alias for resourceinfo in  port_lists.values()]
			PopDialog.comboBox.clear()
			PopDialog.comboBox.addItems(portsnamelist)
			PopDialog.show()
			returns = PopDialog.exec_()
			if returns == PopDialog.Accepted:
				portname = PopDialog.comboBox.currentText() 
				self.text_lists.append('open: '+portname)

				# open port
				results = yield(self.queue_work(self.primary_worker,'open_port', portname))
				self.open_port_button.setText('Close Port')
			else:
				# cancel
				self.text_lists.append('Cancel!!!')
			# open port
			# wait for return 
		else:
			# pop message port already open
			pass
			# self.label.setText(self.dialog.comboBox.currentText())


	# @define_state(MODE_MANUAL, False)
	# def text_test(self,text = ''):
	#	self.text_lists.append('test:'+text)
	#	result = yield(self.queue_work(self.primary_worker,'open_port', 1))
	#	self.text_lists.append('val:'+ str(result))
	#	port_list = self.port_lists()
	#	self.text_lists.append('ports:'+ str(port_list))

	# @define_state(MODE_MANUAL, False)
	# def port_lists(self):
	#	results = yield(self.queue_work(self.primary_worker, 'port_lists'))
	#	if results:
	#		self.text_lists.append('test'+'true')
	#		self.text_lists.append('test'+str(type(results)))
	#		self.text_lists.append('test'+str(len(results)))
	#		self.text_lists.append('test'+str(results))
	#	else:
	#		# nop
	#		pass
	#	return results
	 	
	 	
	# @define_state(MODE_MANUAL,queue_state_indefinitely=True, delete_stale_states=True)
	# def update(self):
	#	step = 480*10**6/2**32
	#	DDS_HEX = self.spinbox_widgets[0].value()/480/10**6*2**32//1
	#	# self.spinbox_widgets[0].setValue(step*DDS_HEX)
	#	self.spinbox_widgets[1].setValue(DDS_HEX)
	#	pass


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
