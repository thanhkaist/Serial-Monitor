# -*- coding: utf-8 -*-
import sys
import math
import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton, QWidget)
from PyQt5.QtWidgets import QInputDialog, QLineEdit

import binascii
class SerialMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super(SerialMonitor, self).__init__()
        # set height and width
        self.resize(800, 600)
        self.port = QSerialPort()
        self.serialDataView = SerialDataView(self)
        self.serialSendView = SerialSendView(self)

        self.setCentralWidget( QtWidgets.QWidget(self) )
        layout = QtWidgets.QVBoxLayout( self.centralWidget() )
        layout.addWidget(self.serialDataView)
        layout.addWidget(self.serialSendView)
        layout.setContentsMargins(3, 3, 3, 3)
        self.setWindowTitle('Serial Monitor')
        self.filterWidget = TextFilterVisualization()
        self.filterWidget.hide()

        ### Tool Bar ###
        self.toolBar = ToolBar(self)
        self.addToolBar(self.toolBar)

        ### Status Bar ###
        self.setStatusBar( QtWidgets.QStatusBar(self) )
        self.statusText = QtWidgets.QLabel(self)
        self.statusBar().addWidget( self.statusText )
        
        ### Signal Connect ###
        self.toolBar.portOpenButton.clicked.connect(self.portOpen)
        self.toolBar.portFilterButton.clicked.connect(self.portFilter)
        self.serialSendView.serialSendSignal.connect(self.sendFromPort)
        self.port.readyRead.connect(self.readFromPort)
    def portFilter(self):
        self.filterWidget.show()

    def portOpen(self, flag):
        if flag:
            self.port.setBaudRate( self.toolBar.baudRate() )
            self.port.setPortName( self.toolBar.portName() )
            self.port.setDataBits( self.toolBar.dataBit() )
            self.port.setParity( self.toolBar.parity() )
            self.port.setStopBits( self.toolBar.stopBit() )
            self.port.setFlowControl( self.toolBar.flowControl() )
            r = self.port.open(QtCore.QIODevice.ReadWrite)
            if not r:
                self.statusText.setText('Port open error')
                self.toolBar.portOpenButton.setChecked(False)
                self.toolBar.serialControlEnable(True)
            else:
                self.statusText.setText('Port opened')
                # change open button text to close
                self.toolBar.portOpenButton.setText('Close')
                self.toolBar.serialControlEnable(False)
        else:
            self.port.close()
            self.statusText.setText('Port closed')
            self.toolBar.portOpenButton.setText('Open')
            self.toolBar.serialControlEnable(True)
        
    def readFromPort(self):
        # check if readline is available
        if (self.port.canReadLine):
            data = self.port.readLine()
            dataString = QtCore.QTextStream(data).readAll()
            # apply some filters
            filter_text_list = self.filterWidget.get_filter_list()
            for filter_text in filter_text_list:
                if filter_text in dataString:
                    return



            if "TX" in dataString:
                self.serialDataView.appendSerialText(dataString, QtGui.QColor(255, 0, 0) )
            elif "RX" in dataString:
                self.serialDataView.appendSerialText(dataString, QtGui.QColor(0, 255, 0) )
            else:
                self.serialDataView.appendSerialText(dataString, QtGui.QColor(0, 0, 255) )
                
        # data = self.port.readAll()
        # if len(data) > 0:

        #     self.serialDataView.appendSerialText( QtCore.QTextStream(data).readAll(), QtGui.QColor(255, 0, 0) )

    def sendFromPort(self, text, hexFlag):
        # Check port is open
        if  self.port.isOpen():
            self.port.write( text.encode("utf-8")) 
            if hexFlag:
                # convert hex to printable string
                self.serialDataView.appendSerialText( text, QtGui.QColor(255, 0, 255) )
            else:
                self.serialDataView.appendSerialText( text, QtGui.QColor(0, 0, 255) )

class SerialDataView(QtWidgets.QWidget):
    def __init__(self, parent):
        super(SerialDataView, self).__init__(parent)
        self.serialData = QtWidgets.QTextEdit(self)
        self.serialData.setReadOnly(True)
        self.serialData.setFontFamily('Courier New')
        self.serialData.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.serialDataHex = QtWidgets.QTextEdit(self)
        self.serialDataHex.setReadOnly(True)
        self.serialDataHex.setFontFamily('Courier New')
        self.serialDataHex.setFixedWidth(500)
        self.serialDataHex.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.label = QtWidgets.QLabel('00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F')
        self.label.setFont( QtGui.QFont('Courier New') )
        self.label.setIndent(5)

        self.setLayout( QtWidgets.QGridLayout(self) )
        self.layout().addWidget(self.serialData,    0, 0, 2, 1)
        self.layout().addWidget(self.label,         0, 1, 1, 1)
        self.layout().addWidget(self.serialDataHex, 1, 1, 1, 1)
        self.layout().setContentsMargins(2, 2, 2, 2)
        
    def appendSerialText(self, appendText, color):
        self.serialData.moveCursor(QtGui.QTextCursor.End)
        self.serialData.setFontFamily('Courier New')
        self.serialData.setTextColor(color)
        self.serialDataHex.moveCursor(QtGui.QTextCursor.End)
        self.serialDataHex.setFontFamily('Courier New')
        self.serialDataHex.setTextColor(color)

        self.serialData.insertPlainText(appendText)
        
        lastData = self.serialDataHex.toPlainText().split('\n')[-1]
        lastLength = math.ceil( len(lastData) / 3 )
        
        appendLists = []
        splitedByTwoChar = re.split( '(..)', appendText.encode().hex() )[1::2]
        if lastLength > 0:
            t = splitedByTwoChar[ : 16-lastLength ] + ['\n']
            appendLists.append( ' '.join(t) )
            splitedByTwoChar = splitedByTwoChar[ 16-lastLength : ]

        appendLists += [ ' '.join(splitedByTwoChar[ i*16 : (i+1)*16 ] + ['\n']) for i in range( math.ceil(len(splitedByTwoChar)/16) ) ]
        if len(appendLists[-1]) < 47:
            appendLists[-1] = appendLists[-1][:-1]

        for insertText in appendLists:
            self.serialDataHex.insertPlainText(insertText)
        
        self.serialData.moveCursor(QtGui.QTextCursor.End)
        self.serialDataHex.moveCursor(QtGui.QTextCursor.End)

class SerialSendView(QtWidgets.QWidget):

    serialSendSignal = QtCore.pyqtSignal(str, bool)

    def __init__(self, parent):
        super(SerialSendView, self).__init__(parent)
        # set implicit height
        self.setFixedHeight(100)

        self.sendData = QtWidgets.QTextEdit(self)
        self.sendData.setAcceptRichText(False)
        self.sendData.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        def on_text_changed():
            sender = self.sender()
            if isinstance(sender, QtWidgets.QTextEdit):
                text = sender.toPlainText()
                if '\n' in text:
                    if sender is self.sendData:
                        self.serialSendSignal.emit( text.replace('\n', ''),False )
                    else:
                        text = text.replace('\n', '')
                        text = text.replace(' ', '')
                        if not re.match( '^[0-9a-fA-F]*$', text ):
                            # use QMessageBox to show error
                            msg = QtWidgets.QMessageBox()
                            msg.setIcon(QtWidgets.QMessageBox.Critical)
                            msg.setText("Text is not in hex format")
                            msg.setWindowTitle("Error")
                            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            msg.exec_()

                            return
                        self.serialSendSignal.emit( binascii.unhexlify(text).decode(),True )
                    #sender.clear()

        # self.sendData.textChanged.connect(on_text_changed)

        self.sendButton = QtWidgets.QPushButton('Send Ascii')
        self.sendButton.clicked.connect(self.sendButtonClicked)
        self.sendButton.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        
        
        self.sendData1 = QtWidgets.QTextEdit(self)
        self.sendData1.setAcceptRichText(False)
        self.sendData1.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.sendData1.textChanged.connect(on_text_changed)
        

        self.sendButton1 = QtWidgets.QPushButton('Send Hex')
        self.sendButton1.clicked.connect(self.sendButtonHexClicked)
        self.sendButton1.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        
        self.setLayout( QtWidgets.QVBoxLayout(self) )
        # Create AsciiBox
        AsciiBox = QtWidgets.QHBoxLayout() # AsciiBox
        AsciiBox.addWidget(self.sendData)
        AsciiBox.addWidget(self.sendButton)
        AsciiBox.setContentsMargins(3, 3, 3, 3)
        # Create HexBox
        HexBox = QtWidgets.QHBoxLayout() # HexBox
        HexBox.addWidget(self.sendData1)
        HexBox.addWidget(self.sendButton1)
        HexBox.setContentsMargins(3, 3, 3, 3)
        # Add AsciiBox and HexBox to layout
        self.layout().addLayout(AsciiBox)
        self.layout().addLayout(HexBox)
        self.layout().setContentsMargins(2, 2, 2, 2)


    def sendButtonClicked(self):
        self.serialSendSignal.emit( self.sendData.toPlainText(),False )
        #self.sendData.clear()
    
    def sendButtonHexClicked(self):
        # remove all spaces
        text = self.sendData1.toPlainText().replace(" ", "")
        # text = text.replace('\n', '')
        if not re.match( '^[0-9a-fA-F]*$', text ):
            self.sendData1.clear()
            # use QMessageBox to show error
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Text is not in hex format")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

            return

        self.serialSendSignal.emit( binascii.unhexlify(text).decode(),True )
        #self.sendData1.clear()

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        
        self.portOpenButton = QtWidgets.QPushButton('Open')
        self.portOpenButton.setCheckable(True)
        self.portOpenButton.setMinimumHeight(32)

        self.portFilterButton = QtWidgets.QPushButton('Filter')
        self.portFilterButton.setCheckable(False)
        self.portFilterButton.setMinimumHeight(32)


        self.portNames = QtWidgets.QComboBox(self)
        self.portNames.addItems([ port.portName() for port in QSerialPortInfo().availablePorts() ])
        if 'COM10' in [self.portNames.itemText(i) for i in range(self.portNames.count())]:
            self.portNames.setCurrentText('COM10')

        self.portNames.setMinimumHeight(30)

        self.baudRates = QtWidgets.QComboBox(self)
        self.baudRates.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', 
            '31250', '38400', '51200', '56000', '57600', '76800', '115200', '128000', '230400', '256000', '921600'
        ])
        self.baudRates.setCurrentText('921600')
        self.baudRates.setMinimumHeight(30)

        self.dataBits = QtWidgets.QComboBox(self)
        self.dataBits.addItems(['5 bit', '6 bit', '7 bit', '8 bit'])
        self.dataBits.setCurrentIndex(3)
        self.dataBits.setMinimumHeight(30)

        self._parity = QtWidgets.QComboBox(self)
        self._parity.addItems(['No Parity', 'Even Parity', 'Odd Parity', 'Space Parity', 'Mark Parity'])
        self._parity.setCurrentIndex(0)
        self._parity.setMinimumHeight(30)

        self.stopBits = QtWidgets.QComboBox(self)
        self.stopBits.addItems(['One Stop', 'One And Half Stop', 'Two Stop'])
        self.stopBits.setCurrentIndex(0)
        self.stopBits.setMinimumHeight(30)

        self._flowControl = QtWidgets.QComboBox(self)
        self._flowControl.addItems(['No Flow Control', 'Hardware Control', 'Software Control'])
        self._flowControl.setCurrentIndex(0)
        self._flowControl.setMinimumHeight(30)

        self.addWidget( self.portOpenButton )
        self.addWidget( self.portNames)
        self.addWidget( self.baudRates)
        self.addWidget( self.dataBits)
        self.addWidget( self._parity)
        self.addWidget( self.stopBits)
        self.addWidget( self._flowControl)
        self.addWidget( self.portFilterButton) 

    def serialControlEnable(self, flag):
        self.portNames.setEnabled(flag)
        self.baudRates.setEnabled(flag)
        self.dataBits.setEnabled(flag)
        self._parity.setEnabled(flag)
        self.stopBits.setEnabled(flag)
        self._flowControl.setEnabled(flag)
        
    def baudRate(self):
        return int(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()

    def dataBit(self):
        return int(self.dataBits.currentIndex() + 5)

    def parity(self):
        return self._parity.currentIndex()

    def stopBit(self):
        return self.stopBits.currentIndex()

    def flowControl(self):
        return self._flowControl.currentIndex()


class TextFilterVisualization(QWidget):
    def __init__(self):
        super().__init__()

        # Create the QLineEdit and QListWidget widgets
        self.filter_input = QLineEdit()
        self.filter_list = QListWidget()

        # Create the "Add", "Remove", and "Clear" buttons
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear")

        # Connect the "Add" button's clicked signal to the add_filter_item slot
        self.add_button.clicked.connect(self.add_filter_item)

        # Connect the "Remove" button's clicked signal to the remove_filter_item slot
        self.remove_button.clicked.connect(self.remove_filter_item)

        # Connect the "Clear" button's clicked signal to the clear_filter_list slot
        self.clear_button.clicked.connect(self.clear_filter_list)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(QLabel("Filter:"), 0, 0)
        layout.addWidget(self.filter_input, 0, 1)
        layout.addWidget(self.add_button, 0, 2)
        layout.addWidget(QLabel("Filter Items:"), 1, 0)
        layout.addWidget(self.filter_list, 2, 0, 1, 3)
        layout.addWidget(self.remove_button, 3, 0)
        layout.addWidget(self.clear_button, 3, 2)

        # Create a central widget and set its layout
        
        self.setLayout(layout)

    def add_filter_item(self):
        # Get the text from the QLineEdit widget
        filter_text = self.filter_input.text()

        # Add the text to the QListWidget
        self.filter_list.addItem(filter_text)

        # Clear the QLineEdit
        self.filter_input.clear()

    def remove_filter_item(self):
        # Get the selected items from the QListWidget
        selected_items = self.filter_list.selectedItems()

        # If there are any selected items, remove them from the QListWidget
        if selected_items:
            for item in selected_items:
                self.filter_list.takeItem(self.filter_list.row(item))

    def clear_filter_list(self):
        # Clear the QListWidget
        self.filter_list.clear()
    def get_filter_list(self):
        # Get the list of items in the QListWidget
        return [self.filter_list.item(i).text() for i in range(self.filter_list.count())]



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

        # Create a password input dialog
    password, ok = QInputDialog.getText(None, "Enter Password", "Password:", QLineEdit.Password)

    if ok:
        # User entered a password and pressed OK
        if (password!="uniconn"):
            # Show an error message if the password is incorrect
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Passwork is not correct!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            sys.exit()
    else:
        sys.exit()

    window = SerialMonitor()
    #Set icon for application using a default serial icon
    app.setWindowIcon( QtGui.QIcon('serial.png') )
    window.show()
    app.exec()
