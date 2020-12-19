from PyQt5 import QtWidgets, QtGui, QtCore


class Ui_MainWindow(object):
    """
    GUI settings
    """
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1281, 766)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("main.ico"), 
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        self.graphicsView = QtWidgets.QGraphicsView(MainWindow)
        self.graphicsView.setGeometry(QtCore.QRect(20, 20, 851, 671))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalScrollBar = QtWidgets.QScrollBar(MainWindow)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(130, 640, 651, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.verticalScrollBar = QtWidgets.QScrollBar(MainWindow)
        self.verticalScrollBar.setGeometry(QtCore.QRect(790, 100, 16, 251))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        
        # Saving of the current figure
        self.savefig = QtWidgets.QPushButton(MainWindow)
        self.savefig.setGeometry(QtCore.QRect(20, 714, 111, 41))
        self.savefig.setObjectName("savefig")
        
        # Settings of pictures scale
        self.logscale = QtWidgets.QCheckBox(MainWindow)
        self.logscale.setGeometry(QtCore.QRect(922, 90, 321, 23))
        self.logscale.setObjectName("logscale")
        
        self.xscale = QtWidgets.QSlider(MainWindow)
        self.xscale.setGeometry(QtCore.QRect(922, 20, 321, 16))
        self.xscale.setOrientation(QtCore.Qt.Horizontal)
        self.xscale.setRange(1, 100)
        self.xscale.setToolTip("Change horizontal scale")
        self.xscale.setPageStep(1)
        self.xscale.setObjectName("xscale")
        self.xscale.valueChanged[int].connect(self.changeValue)
        
        self.yscale = QtWidgets.QSlider(MainWindow)
        self.yscale.setGeometry(QtCore.QRect(922, 60, 321, 16))
        self.yscale.setOrientation(QtCore.Qt.Horizontal)
        self.yscale.setRange(1, 100)
        self.yscale.setToolTip("Change vertical scale")
        self.yscale.setPageStep(1)
        self.yscale.setObjectName("yscale")
        self.yscale.valueChanged[int].connect(self.changeValue)
        
        self.rescale = QtWidgets.QPushButton(MainWindow)
        self.rescale.setGeometry(QtCore.QRect(1130, 90, 111, 25))
        self.rescale.setObjectName("rescale")
        
        # Continuum
        self.showcont = QtWidgets.QCheckBox(MainWindow)
        self.showcont.setGeometry(QtCore.QRect(1020, 140, 151, 23))
        self.showcont.setObjectName("showcont")
        
        self.comboBox = QtWidgets.QComboBox(MainWindow)
        self.comboBox.setGeometry(QtCore.QRect(1040, 170, 51, 21))
        self.comboBox.setObjectName("comboBox")
        for k in range(20):
            self.comboBox.addItem(str(k+1))
            
        self.comboBox_2 = QtWidgets.QComboBox(MainWindow)
        self.comboBox_2.setGeometry(QtCore.QRect(1040, 210, 51, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        for k in range(18):
            self.comboBox_2.addItem(str(5*(k+3)))
        
        self.cont_mode = QtWidgets.QComboBox(MainWindow)
        self.cont_mode.setGeometry(QtCore.QRect(905, 190, 91, 25))
        self.cont_mode.setObjectName("cont_mode")
        self.cont_mode.addItem("Median")
        self.cont_mode.addItem("Envelope")
        
        self.cont = QtWidgets.QPushButton(MainWindow)
        self.cont.setGeometry(QtCore.QRect(1100, 190, 171, 25))
        self.cont.setObjectName("cont")
        
        # Tools for working with lines
        self.masc = QtWidgets.QPushButton(MainWindow)
        self.masc.setGeometry(QtCore.QRect(910, 260, 111, 25))
        self.masc.setObjectName("masc")
        self.gauss = QtWidgets.QPushButton(MainWindow)
        self.gauss.setGeometry(QtCore.QRect(1150, 260, 111, 25))
        self.gauss.setObjectName("gauss")
        self.integrate = QtWidgets.QPushButton(MainWindow)
        self.integrate.setGeometry(QtCore.QRect(1030, 260, 111, 25))
        self.integrate.setObjectName("integrate")
        
        # Table with lines
        self.table = QtWidgets.QTableView(MainWindow)
        self.table.setGeometry(QtCore.QRect(910, 300, 351, 451))
        self.table.setObjectName("table")
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setDefaultSectionSize(166)
        
        self.savetab = QtWidgets.QPushButton(MainWindow)
        self.savetab.setGeometry(QtCore.QRect(140, 714, 111, 41))
        self.savetab.setObjectName("savetab")
        
        # Decorations and widgets style
        self.line = QtWidgets.QFrame(MainWindow)
        self.line.setGeometry(QtCore.QRect(882, 0, 20, 771))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(MainWindow)
        self.line_2.setGeometry(QtCore.QRect(890, 123, 391, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(MainWindow)
        self.line_3.setGeometry(QtCore.QRect(890, 230, 391, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        self.tracking = QtWidgets.QLabel(MainWindow)
        self.tracking.setGeometry(QtCore.QRect(780, 730, 91, 17))
        self.tracking.setObjectName("tracking")
        
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(1010, 170, 41, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(1010, 210, 41, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setGeometry(QtCore.QRect(930, 170, 67, 17))
        self.label_3.setObjectName("label_3")
                
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
            
    def changeValue(self, value):
        return value
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LIAS, version = 0.1"))
        
        self.integrate.setText(_translate("MainWindow", "Integrate"))
        self.logscale.setText(_translate("MainWindow", "Logarithmic scale"))
        self.masc.setText(_translate("MainWindow", "Mass Center"))
        self.cont.setText(_translate("MainWindow", "Recalculate Continuum"))
        self.gauss.setText(_translate("MainWindow", "Fit Gaussian"))
        self.rescale.setText(_translate("MainWindow", "Set Default"))
        self.savefig.setText(_translate("MainWindow", "Save Figure"))
        self.label.setText(_translate("MainWindow", "p ="))
        self.label_2.setText(_translate("MainWindow", "N ="))
        self.label_3.setText(_translate("MainWindow", "Mode:"))
        self.showcont.setText(_translate("MainWindow", "Show Continuum"))
        self.savetab.setText(_translate("MainWindow", "Save Table"))
