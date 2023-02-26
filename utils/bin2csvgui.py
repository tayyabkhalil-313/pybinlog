import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QLabel, QSpinBox
from PyQt5.QtCore import Qt
from .bin2csv import convert2csv
import os

class CheckableComboBox(QComboBox):
	def __init__(self):
		super().__init__()
		self._changed = False
		self.index = 0
		self.activated.connect(self.onActivated)
		self.view().pressed.connect(self.handleItemPressed)

	def onActivated(self, index):
        # check if "Select All" option is selected
		self.index = index
		item = self.model().item(index, self.modelColumn()) 
		if self.itemText(index) == 'Select All':

			for i in range(1, self.count()):
                		item = self.model().item(i, self.modelColumn()) 
                		item0 = self.model().item(0, self.modelColumn()) 
                		if item.checkState() == Qt.Unchecked and item0.checkState() == 2:
                		    item.setCheckState(Qt.Checked)
                		elif item0.checkState() == 0:
                		    item.setCheckState(Qt.Unchecked)

	def setItemChecked(self, index, checked=False):
		item = self.model().item(index, self.modelColumn()) 
	
		if checked:
			item.setCheckState(Qt.Checked)
		else:
			item.setCheckState(Qt.Unchecked)

	def handleItemPressed(self, index):
		item = self.model().itemFromIndex(index)
		
		if item.checkState() == Qt.Checked:
			item.setCheckState(Qt.Unchecked)
		else:
			item.setCheckState(Qt.Checked)
		self._changed = True

	def hidePopup(self):
		if not self._changed:
			super().hidePopup()
		self._changed = False

	def itemChecked(self, index):
		item = self.model().item(index, self.modelColumn())
		return item.checkState() == Qt.Checked

class MyApp(QWidget):
    def __init__(self, parent = None):
        self.messages  = ['ATT', 'BARO', 'MAG', 'ARSP', 'ASM1', 'GPA', 'GPS', 'IMU',
                          'MAV', 'NKF1', 'NKF2', 'NKF3', 'NKF4', 'NKF5', 'NKQ', 'NKT', 'PARM', 
                          'PIDP', 'PIDR', 'PIDY', 'PM', 'SMOO', 'TECS', 'XKF0', 'XKF1', 'XKF2', 'XKF3']
        self.filepath = None
        self.output_directory = None
        super().__init__(parent)
        self.resize(500, 350)
        self.create_widgets()

    def create_widgets(self):
        self.file_button = QPushButton("Select File", self)
        self.file_button.clicked.connect(self.select_file)

        self.message_label = QLabel("Choose messages to convert:", self)
        self.combo = CheckableComboBox()

        self.output_button = QPushButton("Select Output Directory (Optional)", self)
        self.output_button.clicked.connect(self.select_output)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_file)

        self.creator_label = QLabel("Created By: Tayyab Khalil")
        self.creator_label.setFixedSize(150,25)
        self.creator_label.setStyleSheet("background-color: blue; color: white; font-size: 10pt;")

        layout = QVBoxLayout()
        layout.addWidget(self.file_button)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.message_label)
        hbox3.addWidget(self.combo)
        layout.addLayout(hbox3)

        self.combo.addItem('Select All')
        self.combo.setItemChecked(0, False)
        for i in range(len(self.messages)):
            self.combo.addItem(self.messages[i])
            self.combo.setItemChecked(i + 1, False)

        layout.addWidget(self.output_button)

        layout.addWidget(self.convert_button)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.creator_label)
        layout.addLayout(hbox4)

        self.setLayout(layout)

    def select_file(self):
        self.filepath, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Log Files (*.bin)")
        self.file_button.setText("Selected File '" + os.path.basename(self.filepath) + "'")
        self.file_button.setStyleSheet("background-color: green")
        print(f"Selected file: {self.filepath}")

    def select_output(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        print(f"Selected directory: {self.output_directory}")

    def convert_file(self):
        if self.filepath is None:
            self.convert_button.setText("Please select a file for conversion.")
            self.convert_button.setStyleSheet("background-color: red")
        else:
            convert2csv(self.filepath, self.getMessages(), self.output_directory)
            self.convert_button.setText("File Converted")
            self.convert_button.setStyleSheet("background-color: green")

            print("File converted!")
	
    def getfilepath(self):
	    return self.filepath
    
    def getValue(self):
        items_checked = []
        for i in range(len(self.messages)):
            #print('Index: {0} is checked {1}'.format(i, self.combo.itemChecked(i)))
            if self.combo.itemChecked(i+1):
                items_checked.append(self.messages[i])
        return items_checked
    
    def getMessages(self):
	    messages_checked = self.getValue()
	    return ', '.join(messages_checked)

def main():
	app = QApplication(sys.argv)

	myApp = MyApp()
	myApp.show()
	
	app.exit(app.exec_())
