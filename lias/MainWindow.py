import numpy as np
import matplotlib.pyplot as plt

import UI_MainWindow
import PandasModel
import Tools

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.widgets import SpanSelector


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for showing object and atomic spectra and working with lines
    -----------------------------
    spec - Spectra class instance
    Output window: 1) Upper panel - object spectrum
                   2) Lower panel - atomic spectrum on the same range
                   3) Table - dataframe with founded lines
                   4) In the upper right corner - graphs scale settings
    """      
    
    def find_area(self, line_num):
        """
        Find selected area
        """
    
        ns = np.array(
            np.abs(self.spec.Object_Spectrum[:, 0] - self.selection[line_num, 0])
        ).argmin()
        nf = np.array(
            np.abs(self.spec.Object_Spectrum[:, 0] - self.selection[line_num, 1])
        ).argmin()
           
        wln_sel = self.spec.Object_Spectrum[ns:nf, 0]
        flx_sel = self.spec.Object_Spectrum[ns:nf, 1]
        cnt_sel = self.cont[ns:nf]
        cnt_lvl = np.median(cnt_sel)
        
        return wln_sel, flx_sel, cnt_sel, cnt_lvl
            
    def continuum(self):
        """
        Trying to find continuum in current spectrum
        """
        
        deg = self.ui.comboBox.currentIndex() + 1
        num = 5*(self.ui.comboBox_2.currentIndex()+3)
        mode = self.ui.cont_mode.currentIndex()        
        spectr = [[sp_point[0], sp_point[1]]
                  for sp_point in self.spec.Object_Spectrum]
            
        split = np.array_split(spectr, num)
        cont_point = []
        for part in split:
            if mode == 0:
                value = np.median(part[:, 1])
            else:
                value = np.max(part[:, 1])
            
            ind = np.abs(part[:, 1] - value).argmin()
            cont_point.append([part[ind, 0], part[ind, 1]])
        
        self.cont = Tools.calc_cont(cont_point, deg)

        return cont_point, self.cont
                           
    def masc(self):
        """
        Function for calculation of mass center of selected area 
        """
        
        try:
            num = self.k
            
        except AttributeError:
            pass
            
        else:
            wln_sel, flx_sel, cnt_sel, cnt_lvl = self.find_area(num)

            mc = Tools.calc_masc(wln_sel, flx_sel)
            theor = self.atomicdata['Wavelength, Å'].iloc[num]
            
            self.atomicdata['Obs. wavelength'].iloc[num] = mc
            self.atomicdata['Obs. - Theor.'].iloc[num] = mc - theor
            self.model = PandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.rescale()
        
    def intense(self):
        """
        Function for calculation area between spectrum and continuum 
        in selected area
        """
        try:
            num = self.k
            
        except AttributeError:
            pass
            
        else:
            wln_sel, flx_sel, cnt_sel, cnt_lvl = self.find_area(num)
            
            intensity = Tools.calc_int(wln_sel, flx_sel, cnt_sel)

            self.atomicdata['Intensity'].iloc[num] = intensity
            self.model = PandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            self.ax1.fill_between(wln_sel, flx_sel, cnt_sel, color='w')
            
            self.canvas.draw()
        
    def gauss(self):
        """
        Function to fitting gaussian in selected area
        """
        
        try:
            num = self.k
            
        except AttributeError:
            pass
        
        else:    
            wln_sel, flx_sel, cnt_sel, cnt_lvl = self.find_area(num)
            
            popt = Tools.fit_gauss(wln_sel, flx_sel, cnt_lvl)
            
            self.ax1.plot(
                wln_sel, 
                Tools.gauss_function(wln_sel, *popt) + cnt_lvl,
                color='#fc5a50'
            )
            
            theor = self.atomicdata['Wavelength, Å'].iloc[num]
            self.atomicdata['Obs. wavelength (Gauss)'].iloc[num] = popt[1]
            self.atomicdata['Obs.-Theor. (Gauss)'].iloc[num] = popt[1] - theor
            fwhm = 2 * np.sqrt(2 * np.log(2)) * popt[2]
            self.atomicdata['FWHM (Gauss)'].iloc[num] = fwhm
            intense = np.trapz(Tools.gauss_function(wln_sel, *popt), wln_sel)
            self.atomicdata['Intensity (Gauss)'].iloc[num] = intense
            self.model = PandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.canvas.draw()
    
    def RGB(self, wavelength):
        """
        Function for transformation wavelength in angstroms to RGB-color
        (lines outside the visible range are assigned gray)
        """    
         
        wl = wavelength/10   
        
        if 380 < wl <= 440:
            B = 0.3 + 0.7*(wl - 380)/(440 - 380)
            R, G = B*(440 - wl)/(440 - 380), 0
            
        elif 440 < wl <= 490:
            R, G, B = 0., (wl - 440)/(490 - 440), 1.
            
        elif 490 < wl <= 510:
            R, G, B = 0., 1., (510 - wl)/(510 - 490)
            
        elif 510 < wl <= 580:
            R, G, B = (wl - 510)/(580 - 510), 1., 0.
            
        elif 580 < wl <= 645:
            R, G, B = 1., (645 - wl)/(645 - 580), 0.
            
        elif 645 < wl <= 750:
            R, G, B = 0.3 + 0.7*(750 - wl)/(750 - 645), 0., 0.
            
        else:
            R, G, B = 0.5, 0.5, 0.5       
                 
        return R, G, B  
        
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
        low_w = self.spec.Object_Spectrum[left, 0]
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
        ax2.set_ylim([0.0, 2.1])
        self.ax1.set_xlim(low_w, upp_w)
        ax2.set_xlim([low_w, upp_w])  
        cnt = self.ui.showcont.checkState()
        cont_point, cont = self.continuum() 
        
        if lsc == 2:
            self.ax1.semilogy(self.spec.Object_Spectrum[:, 0],
                              self.spec.Object_Spectrum[:, 1],
                              '-', color='#fff9d0')
            if cnt == 2:
                self.ax1.semilogy(self.spec.Object_Spectrum[:, 0],
                                  cont, '-', color='#98eff9')
             
        else:
            self.ax1.plot(self.spec.Object_Spectrum[:, 0],
                          self.spec.Object_Spectrum[:, 1],
                          '-', color='#fff9d0')
            if cnt == 2:
                self.ax1.plot(self.spec.Object_Spectrum[:, 0],
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
                    color=self.calc_RGB(swl[2]),
                    alpha=0.3
                )
                
        for i in range(len(self.atomicdata['Wavelength, Å'])):
            df = self.atomicdata.iloc[i]
            if df['Obs. wavelength'] != '':
                self.ax1.axvline(df['Obs. wavelength'],
                                 color=self.calc_RGB(df['Wavelength, Å']))
        
        for point in cont_point:
            if cnt == 2:
                self.ax1.scatter(point[0], point[1], 
                                 marker='x', color='#fc5a50', s=50)
            
        a_max = np.max(self.atomicdata['A_ki'])
        for i in range(len(self.atomicdata['Wavelength, Å'])):
            df = self.atomicdata.iloc[i]
            wl = df['Wavelength, Å']
            a = df['A_ki']
            col = self.calc_RGB(wl)
          
            if df['Type'] == "":
                tr = 0.9*a/a_max + 0.1
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
            num = self.k
            
        except AttributeError:
            pass
        
        else:
            self.selection[num] = [xmin, xmax, 
                                   self.atomicdata['Wavelength, Å'].iloc[num]] 
            self.atomicdata['Obs. wavelength'].iloc[num] = ''
            self.atomicdata['Obs. - Theor.'].iloc[num] = ''
            self.atomicdata['Intensity'].iloc[num] = ''
            self.atomicdata['Obs. wavelength (Gauss)'].iloc[num] = ''
            self.atomicdata['Obs.-Theor. (Gauss)'].iloc[num] = ''
            self.atomicdata['FWHM (Gauss)'].iloc[num] = ''
            self.atomicdata['Intensity (Gauss)'].iloc[num] = ''
            self.model = PandasModel(self.atomicdata)
            self.ui.table.setModel(self.model)
            
            self.rescale()
        
    def table_DoubleClicked(self):
        """
        Selection of line in table (by double mouse click)
        """

        row = self.ui.table.selectionModel().selectedRows()
        self.k = row[0].row()
        
    def __init__(self, spec):       
        super().__init__()
        self.ui = UI_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)  
        
        wln_min = spec.Object_Spectrum[0, 0]
        wln_max = spec.Object_Spectrum[-1, 0]
        self.wln_step = (wln_max - wln_min)/len(spec.Object_Spectrum[:, 0])
        
        self.atomicdata = spec.Atomic_Data
        self.atomicdata['Obs. wavelength'] = ''
        self.atomicdata['Obs. - Theor.'] = ''
        self.atomicdata['Intensity'] = ''
        self.atomicdata['Obs. wavelength (Gauss)'] = ''
        self.atomicdata['Obs.-Theor. (Gauss)'] = ''
        self.atomicdata['FWHM (Gauss)'] = ''
        self.atomicdata['Intensity (Gauss)'] = ''
        self.model = PandasModel(self.atomicdata)
        self.ui.table.setModel(self.model)
        self.ui.table.doubleClicked.connect(self.table_DoubleClicked)
        
        self.spec = spec       
        self.low_w0 = spec.Object_Spectrum[0, 0]
        self.upp_w0 = spec.Object_Spectrum[-1, 0]
        self.up_to_low0 = self.upp_w0 - self.low_w0
        
        self.fig = plt.figure(figsize=(8, 6.5))
        self.selection = np.zeros(shape=(len(spec.Object_Spectrum[:, 0]), 3))
        self.canvas = FigureCanvasQTAgg(self.fig)
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
        self.ui.masc.clicked.connect(self.masc)
        self.ui.integrate.clicked.connect(self.intense)
        self.ui.gauss.clicked.connect(self.fit_gauss)
        self.ui.savefig.clicked.connect(self.save_figure) 
        self.ui.savetab.clicked.connect(self.save_table)
