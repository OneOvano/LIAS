import lias
from numpy import loadtxt

def main(filename, ion):
    spec = loadtxt(filename)
    sp = Spectra(spec, ion)
    DoWork(sp)
