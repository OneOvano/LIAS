from lias import *
from numpy import loadtxt

# Example
spectrum = loadtxt('CX_Cep.dat')
sp = Spectra(spectrum, 'N IV')
sp.describe()
sp.print_NIST()
DoWork(sp)        
