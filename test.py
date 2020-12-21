import lias

import unittest
import numpy as np


class test_spectra(unittest.TestCase):
    """
    Testing of parser and Spectra methods
    """

    def test_load(self):
        o_iii = lias._load('O III', 6500, 6600)
        o_iii = o_iii.to_dict('list')
        target = {
            'Wavelength, Å': [6507.55],
            'A_ki': [39800000.0],
            'Lower Level Term': ['1P'],
            'Lower Level J': [1.0],
            'Upper Level Term': ['1P°'],
            'Upper Level J': [1.0],
            'Type': ['']
        }
        assert o_iii == target

    def test_spec(self):
        spectrum = np.array([[6500., 1.0], [6660., 1.0]])
        sp = lias.Spectra(spectrum, 'O III')
        target = sp.Object_Spectrum
        np.testing.assert_equal(spectrum, target)
        

class test_tools(unittest.TestCase):
    """
    Testing of the tools for working with lines
    """

    def test_calc_cont(self):
        x = [6500, 6600]
        y = [1., 1.]
        wln = 6550
        target = 1.
        np.testing.assert_allclose(lias.Tools.calc_cont(x, y, wln, 1), target)

    def test_masc(self):
        x = np.array([1., 2., 3.])
        y = np.array([0., 1., 0.])
        target = 2.
        np.testing.assert_allclose(lias.Tools.calc_masc(x, y), target)

    def test_intense(self):
        x = np.linspace(0, 1, 100)
        y = x**3
        cnt = np.linspace(0, 0, 100)
        target = 0.25
        np.testing.assert_allclose(lias.Tools.calc_int(x, y, cnt), target)

    def test_gauss(self):
        x = np.linspace(-1, 1, 100)
        target = (1., 0., 0.5)
        y = lias.Tools.gauss_function(x, *target)
        cnt = 0
        output = lias.Tools.fit_gauss(x, y, cnt)
        accuracy = np.abs(np.array(output - target))
        np.testing.assert_allclose(accuracy, target)


if __name__ == '__main__':
    unittest.main()
