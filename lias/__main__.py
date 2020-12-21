import sys
import lias
import numpy as np

def main(filename, ion):
    spec = np.loadtxt(filename)
    sp = Spectra(spec, ion)
    DoWork(sp)

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1])
