import sys
import numpy as np
from lias import *

def main(filename, ion):
    spec = np.loadtxt(filename)
    sp = Spectra(spec, ion)
    DoWork(sp)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
