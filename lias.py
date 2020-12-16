"""
    >>>>>>> LIAS == Lines Indentification in Astrophysical Spectra <<<<<<<
    Prototype of a software package for the identification of atomic lines 
in the astrophysical objects spectra (with using NIST Atomic Spectra Database)
"""

import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui, QtCore
from urllib.parse import urlencode
from scipy.optimize import curve_fit

from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qt5agg import FigureCanvas

pd.options.mode.chained_assignment = None


__author__ = 'Vano'
__version__ = '0.1'


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
        
        ### Saving of the current figure ###
        self.savefig = QtWidgets.QPushButton(MainWindow)
        self.savefig.setGeometry(QtCore.QRect(20, 714, 111, 41))
        self.savefig.setObjectName("savefig")
        
        ### Settings of pictures scale ###
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
        
        ### Continuum ###
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
        
        ### Tools for working with lines ###
        self.masc = QtWidgets.QPushButton(MainWindow)
        self.masc.setGeometry(QtCore.QRect(910, 260, 111, 25))
        self.masc.setObjectName("masc")
        self.gauss = QtWidgets.QPushButton(MainWindow)
        self.gauss.setGeometry(QtCore.QRect(1150, 260, 111, 25))
        self.gauss.setObjectName("gauss")
        self.integrate = QtWidgets.QPushButton(MainWindow)
        self.integrate.setGeometry(QtCore.QRect(1030, 260, 111, 25))
        self.integrate.setObjectName("integrate")
        
        ### Table with lines ###
        self.table = QtWidgets.QTableView(MainWindow)
        self.table.setGeometry(QtCore.QRect(910, 300, 351, 451))
        self.table.setObjectName("table")
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setDefaultSectionSize(166)
        
        self.savetab = QtWidgets.QPushButton(MainWindow)
        self.savetab.setGeometry(QtCore.QRect(140, 714, 111, 41))
        self.savetab.setObjectName("savetab")
        
        ### Decorations and widgets style ###
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
   
        
class Spectra:
    """
    Loading of object spectrum and atomic data from NIST database
    -------------------------------------------------------------  
    Object_Spectrum - path to file with object spectrum (ASCII with two columns)
    Atomic_Data - keys to atomic spectrum - element and ionization degree
    (e.g. 'He II', all available values you can see on NIST website)
    """
    
    def _load(self, ion, low_w, upp_w, allowed_out=1, forbid_out=1):
        """
        Parser for downloading atomic data from NIST server
        ---------------------------------------------------
        ion - key from Atomic_Data (element and ionisation degree)
        low_v and upp_v - limits of wavelength range (define automatically as the
                                           consequences range of Object_Spectrum)
        """
        nist_db_URL = 'http://physics.nist.gov/cgi-bin/ASD/lines1.pl?'
        settings = {
            'spectra': ion,
            'low_w': low_w,
            'upp_w': upp_w,
            'unit': 0,
            'line_out': 0,
            'show_calc_wl': 1,
            'show_av': 0,
            'tsb_value': 1,
            'allowed_out': allowed_out,
            'forbid_out': forbid_out,
            'term_out': 'on',
            'J_out': 'on'
        }
        
        URL = nist_db_URL + urlencode(settings)
        
        df = pd.read_html(URL)
        df = pd.DataFrame(df[3])
        df.drop(['Acc.'], axis='columns', inplace=True)
        df.columns = [
            'Wavelength, Å', 'A_ki',
            'Lower Level Term', 'Lower Level J',
            'Upper Level Term', 'Upper Level J',
            'Type'
        ]
        df.dropna(how='all', inplace=True)
        df['A_ki'].fillna(0, inplace=True)
        df.fillna("", inplace=True)
        df['Wavelength, Å'] = [np.float(line.replace(" ",""))
                               for line in df['Wavelength, Å']]
        atomic_data = df
        return atomic_data                
                         
    def describe(self):
        """
        Description with spectrum characteristic
        ----------------------------------------
        Spectral range - minimal and maximal wavelength
        Wavelength step Δλ
        Spectral resolution by formula R = <λ>/Δλ
        Mean continuum level as a median averaging
        """
        
        wln_min = self.Object_Spectrum[0,0]
        wln_max = self.Object_Spectrum[-1,0]
        wln_step = (wln_max - wln_min)/len(self.Object_Spectrum[:,0])
        resol = 0.5*(wln_min + wln_max)/wln_step
        cont = np.median(self.Object_Spectrum[:,1])
        print(
            "\n\tSpectrum description:\n" +
            "Minimal wavelength:\t{:.4f}".format(wln_min) + " Å\n" +
            "Maximal wavelength:\t{:.4f}".format(wln_max) + " Å\n" +
            "Wavelength step:\t{:.4f}".format(wln_step) + " Å\n" +
            "Average resolution:\t{:.4f}".format(resol)+"\n" +
            "Median flux level:\t{:.4e}".format(cont) + " flux units\n"
        )
    
    def print_NIST(self):
        """
        Print table with lines in console
        """
        print(self.Atomic_Data)
    
    def ion_key(self, ion):
        return ion
                 
    def __init__(self, Object_Spectrum, Atomic_Data):
        self.ion = self.ion_key(Atomic_Data)
        self.Object_Spectrum = np.array(Object_Spectrum)
        low_w = self.Object_Spectrum[0,0]
        upp_w = self.Object_Spectrum[-1,0]
        self.Atomic_Data = self._load(self.ion, low_w, upp_w)


class pandasModel(QtCore.QAbstractTableModel):
    """
    Model for display table with atomic data
    """
    
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
                
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
            
        return None
    
            
class MainWindow(QtWidgets.QMainWindow):
    """
    Class for showing object and atomic spectra and working with lines
    ------------------------------
    spec - Spectra class instance
    Output window: 1) Upper panel - object spectrum
                   2) Lower panel - atomic spectrum on the same range
                   3) Table - dataframe with founded lines
                   4) In the upper right corner - graphs scale settings
    """      
    
    def calc_RGB(self, wavelength):
        """
        Function for transformation wavelength in angstroms to RGB-color
        (lines outside the visible range are assigned gray)
        """     
        wl = wavelength/10   
        
        if (380 < wl <= 440):
            B = 0.3 + 0.7*(wl - 380)/(440 - 380)
            R, G = B*(440 - wl)/(440 - 380), 0
            
        elif (440 < wl <= 490):
            R, G, B = 0., (wl - 440)/(490 - 440), 1.
            
        elif (490 < wl <= 510):
            R, G, B = 0., 1., (510 - wl)/(510 - 490)
            
        elif (510 < wl <= 580):
            R, G, B = (wl - 510)/(580 - 510), 1., 0.
            
        elif (580 < wl <= 645):
            R, G, B = 1., (645 - wl)/(645 - 580), 0.
            
        elif (645 < wl <= 750):
            R, G, B = 0.3 + 0.7*(750 - wl)/(750 - 645), 0., 0.
            
        else:
            R, G, B = 0.5, 0.5, 0.5       
                 
        return (R, G, B)  
        
    def continuum(self):
        """
        Trying to find continuum in current spectrum
        """
        deg = self.ui.comboBox.currentIndex() + 1
        num = 5*(self.ui.comboBox_2.currentIndex()+3)
        mode = self.ui.cont_mode.currentIndex()        
        spectr = []
        for k in range(len(self.spec.Object_Spectrum[:,0])):
            spectr.append([self.spec.Object_Spectrum[k,0], 
                          self.spec.Object_Spectrum[k,1]])
            
        split = np.array_split(spectr, num)
        cont_point = []
        for k in range(num):
            if mode == 0:
                value = np.median(split[k][:,1])
            else:
                value = np.max(split[k][:,1])
            
            ind = np.abs(split[k][:,1] - value).argmin()
            cont_point.append([split[k][ind,0], split[k][ind,1]])
        
        x, y = [], []
        for point in cont_point:
            x.append(point[0])
            y.append(point[1])
            
        cont_coef = np.polyfit(x, y, deg)
        self.cont  = np.sum(cont_coef[-p-1]*self.spec.Object_Spectrum[:,0]**p 
                            for p in range(len(cont_coef)))
        return cont_point, self.cont
    
    def update_canvas(self, low_w, upp_w, lsc): 
        """
        Function for drawing plots
        """
        plt.clf()
               
        title = "Object spectrum and line identification plot for "
        title = title + self.spec.ion
        self.fig.suptitle(title, fontsize=15) 
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_facecolor('k')     
        ax2 = self.fig.add_subplot(212)
        ax2.get_yaxis().set_visible(False)
        ax2.set_facecolor('k')
        ax2.set_ylim([0.0,2.1]) 
        self.ax1.set_xlim(low_w, upp_w)
        ax2.set_xlim([low_w, upp_w])  
        cnt = self.ui.showcont.checkState()
        cont_point, cont = self.continuum() 
        
        if lsc == 2:
            self.ax1.semilogy(self.spec.Object_Spectrum[:,0], 
                              self.spec.Object_Spectrum[:,1], 
                              '-', color='#fff9d0')
            if cnt == 2:
                self.ax1.semilogy(self.spec.Object_Spectrum[:,0], 
                                  cont, '-', color='#98eff9')
             
        else:
            self.ax1.plot(self.spec.Object_Spectrum[:,0], 
                          self.spec.Object_Spectrum[:,1], 
                          '-', color='#fff9d0')
            if cnt == 2:
                self.ax1.plot(self.spec.Object_Spectrum[:,0], 
                              cont, '-', color='#98eff9')
                   
        ysc = self.ui.yscale.value()
        self.ui.verticalScrollBar.setRange(0, ysc-1) 
        place = self.ui.verticalScrollBar.value()
        def_ylim = self.ax1.get_ylim()
        upp_to_low_y = (def_ylim[1] - def_ylim[0])*(101 - ysc)/100
        upp_y = def_ylim[1] - (def_ylim[1] - def_ylim[0] - upp_to_low_y) * (place/ysc)
        low_y = upp_y - upp_to_low_y
        self.ax1.set_ylim([low_y, upp_y])
        
        for swl in self.selection:
            if swl.all() != 0:
                self.ax1.axvspan(
                    swl[0], 
                    swl[1], 
                    color = self.calc_RGB(swl[2]), 
                    alpha=0.3
                )
                
        for i in range(len(self.atomicdata['Wavelength, Å'])):
            df = self.atomicdata.iloc[i]
            if df['Obs. wavelength'] != '':
                self.ax1.axvline(df['Obs. wavelength'],
                                 color = self.calc_RGB(df['Wavelength, Å']))
        
        for point in cont_point:
            if cnt == 2:
                self.ax1.scatter(point[0], point[1], 
                                 marker='x', color='#fc5a50', s=50)
            
        A_max = np.max(self.atomicdata['A_ki'])
        for i in range(len(self.atomicdata['Wavelength, Å'])):
            df = self.atomicdata.iloc[i]
            wl = df['Wavelength, Å']
            A = df['A_ki']
            col = self.calc_RGB(wl)
          
            if (df['Type'] == ""):
                tr = 0.9*A/A_max + 0.1
                ax2.scatter(wl, 1., color=col, marker='|', s=14000, alpha=tr)
            else:
                tr = 1.
                ax2.scatter(wl, 1., color=col, marker='|', s=14000, alpha=tr)
                ax2.scatter(wl, 0.05, color=col, marker='|', s=50)               
        
        self.span = SpanSelector(
            self.ax1, 
            self.onselect, 
            'horizontal', 
            useblit=True,
            rectprops=dict(alpha=0.3, facecolor='red')
        )               
        self.canvas.draw()
    
    def rescale(self):
        """
        Setting of graph scale
        """
        xsc = self.ui.xscale.value()
        lsc = self.ui.logscale.checkState()
        up_to_low = (self.upp_w0 - self.low_w0)*(101 - xsc)/100     
        wind = np.ceil((self.up_to_low0 - up_to_low)/self.wln_step)
        self.ui.horizontalScrollBar.setRange(0, wind) 
        left = self.ui.horizontalScrollBar.value()
        low_w = self.spec.Object_Spectrum[left,0]
        upp_w = low_w + up_to_low
        self.update_canvas(low_w, upp_w, lsc)       
        
    def rescale_OK(self):
        """
        Rescale graph corresponding to default settings 
        """
        self.ui.xscale.setValue(1)
        self.ui.yscale.setValue(1)
        self.ui.logscale.setCheckState(QtCore.Qt.Unchecked)
        self.ui.horizontalScrollBar.setRange(0, 0)
        self.ui.verticalScrollBar.setRange(0, 0)
        self.update_canvas(self.low_w0, self.upp_w0, 0)
        
    def save_figure(self):
        """
        Saver for current figure
        """
        try:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, 
                "LIAS Save figure",
                "", 
                "PNG file (*.png)"
            )
            plt.savefig(filename)
            
        except FileNotFoundError:
            pass
            
    def save_table(self):
        """
        Saver for current figure
        """
        try:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, 
                "LIAS Save Lines",
                "", 
                "CSV  (*.csv)"
            )
            self.atomicdata.to_csv(filename)
            
        except FileNotFoundError:
            pass             
        
    def mouse_place(self, event):
        """
        Tracker of mouse place on graph
        """
        if event.inaxes is None:
            text = ""
        else:
            text = "x = " + "{:.4f}".format(event.xdata)
            
        self.ui.tracking.setText(text)
        return event.xdata
        
    def onselect(self, xmin, xmax):
        """
        Drawing the selected area on graph
        """
        try:
            self.selection[self.k] = [xmin, xmax, 
                                      self.atomicdata['Wavelength, Å'].iloc[self.k]] 
            self.atomicdata['Obs. wavelength'].iloc[self.k] = ''
            self.atomicdata['Obs. - Theor.'].iloc[self.k] = ''
            self.atomicdata['Intensity'].iloc[self.k] = ''
            self.atomicdata['Obs. wavelength (Gauss)'].iloc[self.k] = ''
            self.atomicdata['Obs.-Theor. (Gauss)'].iloc[self.k] = ''
            self.atomicdata['FWHM (Gauss)'].iloc[self.k] = ''
            self.atomicdata['Intensity (Gauss)'].iloc[self.k] = ''
            self.model = pandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.rescale()
            
        except:
            pass
        
    def table_DoubleClicked(self):
        """
        Selection of line in table (by double mouse click)
        """
        row = self.ui.table.selectionModel().selectedRows()
        self.k = row[0].row()
                           
    def calc_masc(self):
        """
        Function for calculation of mass center of selected area 
        """
        try:
            ns = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,0])
            ).argmin()
            nf = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,1])
            ).argmin()
            
            wln_sel = self.spec.Object_Spectrum[ns:nf,0]
            flx_sel = self.spec.Object_Spectrum[ns:nf,1]
            mx = np.sum(wln_sel[k] * flx_sel[k] for k in range(nf - ns))
            m = np.sum(flx_sel)   
            mc = mx / m
            theor = self.atomicdata['Wavelength, Å'].iloc[self.k]
            
            self.atomicdata['Obs. wavelength'].iloc[self.k] = mc
            self.atomicdata['Obs. - Theor.'].iloc[self.k] = mc - theor
            self.model = pandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.rescale()
            
        except:
            pass
        
    def calc_int(self):
        """
        Function for calculation area between spectrum and continuum 
        in selected area
        """
        try:
            ns = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,0])
            ).argmin()
            nf = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,1])
            ).argmin()
            
            wln_sel = self.spec.Object_Spectrum[ns:nf,0]
            flx_sel = self.spec.Object_Spectrum[ns:nf,1]
            cnt_sel = self.cont[ns:nf]
            
            intense = np.trapz(flx_sel - cnt_sel, wln_sel)
            self.atomicdata['Intensity'].iloc[self.k] = intense
            self.model = pandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            self.ax1.fill_between(wln_sel, flx_sel, cnt_sel, color='w')
            
            self.canvas.draw()
            
        except:
            pass
        
    def fit_gauss(self):
        """
        Function to fitting gaussian in selected area
        """
        try:
            def gauss_function(x, a, x0, sigma):
                return a * np.exp(-(x - x0)**2 / (2 * sigma**2))
                
            ns = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,0])
            ).argmin()
            nf = np.array(
                np.abs(self.spec.Object_Spectrum[:,0] - self.selection[self.k,1])
            ).argmin()
            
            wln_sel = self.spec.Object_Spectrum[ns:nf,0]
            flx_sel = self.spec.Object_Spectrum[ns:nf,1]
            cnt_sel = self.cont[ns:nf]
            cnt_lvl = np.median(cnt_sel)
            
            amp = np.max(flx_sel) - np.min(flx_sel)
            mx = np.sum(wln_sel[k] * flx_sel[k] for k in range(nf - ns))
            m = np.sum(flx_sel)   
            mean = mx / m
            sigma = np.std(flx_sel)
            
            popt, pcov = curve_fit(
                gauss_function, 
                wln_sel, 
                flx_sel - cnt_lvl, 
                p0 = [amp, mean, sigma]
            )
            
            self.ax1.plot(
                wln_sel, 
                gauss_function(wln_sel, *popt) + cnt_lvl, 
                color='#fc5a50'
            )
            
            theor = self.atomicdata['Wavelength, Å'].iloc[self.k]
            self.atomicdata['Obs. wavelength (Gauss)'].iloc[self.k] = popt[1]
            self.atomicdata['Obs.-Theor. (Gauss)'].iloc[self.k] = popt[1] - theor
            fwhm = 2 * np.sqrt(2 * np.log(2)) * popt[2]
            self.atomicdata['FWHM (Gauss)'].iloc[self.k] = fwhm
            intense = np.trapz(gauss_function(wln_sel, *popt), wln_sel)
            self.atomicdata['Intensity (Gauss)'].iloc[self.k] = intense
            self.model = pandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.canvas.draw()
            
        except:
            pass
        
    def __init__(self, spec):       
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        
        wln_min = spec.Object_Spectrum[0,0]
        wln_max = spec.Object_Spectrum[-1,0]
        self.wln_step = (wln_max - wln_min)/len(spec.Object_Spectrum[:,0])
        
        self.atomicdata = spec.Atomic_Data
        self.atomicdata['Obs. wavelength'] = ''
        self.atomicdata['Obs. - Theor.'] = ''
        self.atomicdata['Intensity'] = ''
        self.atomicdata['Obs. wavelength (Gauss)'] = ''
        self.atomicdata['Obs.-Theor. (Gauss)'] = ''
        self.atomicdata['FWHM (Gauss)'] = ''
        self.atomicdata['Intensity (Gauss)'] = ''
        self.model = pandasModel(self.atomicdata)
        self.ui.table.setModel(self.model)
        self.ui.table.doubleClicked.connect(self.table_DoubleClicked)
        
        self.spec = spec       
        self.low_w0 = spec.Object_Spectrum[0,0]
        self.upp_w0 = spec.Object_Spectrum[-1,0]
        self.up_to_low0 = self.upp_w0 - self.low_w0
        
        self.fig = plt.figure(figsize = (8, 6.5))
        self.selection = np.zeros(shape = (len(spec.Object_Spectrum[:,0]),3))
        self.canvas = FigureCanvas(self.fig)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addWidget(self.canvas)
        self.ui.graphicsView.setScene(scene)
        
        self.mouse_event = self.canvas.mpl_connect('motion_notify_event', 
                                                   self.mouse_place)
        self.ui.savefig.clicked.connect(self.save_figure)
        self.rescale_OK()
        
        self.ui.horizontalScrollBar.valueChanged.connect(self.rescale)
        self.ui.verticalScrollBar.valueChanged.connect(self.rescale)
        self.ui.xscale.valueChanged.connect(self.rescale)
        self.ui.yscale.valueChanged.connect(self.rescale)
        self.ui.logscale.stateChanged.connect(self.rescale)
        self.ui.rescale.clicked.connect(self.rescale_OK)
        
        self.ui.showcont.stateChanged.connect(self.rescale)
        self.ui.cont.clicked.connect(self.rescale)
        self.ui.masc.clicked.connect(self.calc_masc)
        self.ui.integrate.clicked.connect(self.calc_int)
        self.ui.gauss.clicked.connect(self.fit_gauss)
        self.ui.savefig.clicked.connect(self.save_figure) 
        self.ui.savetab.clicked.connect(self.save_table)          


class DoWork:
    """
    Show the main window and do work
    """
    
    def __init__(self, spec):
        app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow(spec)
        mainWin.show()    
        sys.exit(app.exec_())
                
