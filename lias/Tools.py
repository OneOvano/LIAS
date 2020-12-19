"""Functions for working with lines in spectrum"""

import numpy as np
from scipy.optimize import curve_fit


def gauss_function(x, a, x0, sigma):
    """
    Gaussian
    _________
    Arguments:

    x (float or float array) - argument
    a (float) - amplitude
    x0 (float) - mathematical expectation
    sigma (float) - standard deviation
    __________________________________
    Returns:

    Gauss function by formula
    a * np.exp(-(x - x0)**2 / (2 * sigma**2))
    """

    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))


def calc_cont(points, deg):
    """
    Trying to find continuum in current spectrum
    ____________________________________________
    Arguments:

    points (float x float array) - selected points
    deg - polynome degree
    _____________________
    Returns:

    Continuum curve
    """

    cont_coef = np.polyfit(points[:, 0], points[:, 1], deg)
    cont = np.poly1d(cont_coef)(points[:, 0])

    return cont


def calc_masc(wln_sel, flx_sel):
    """
    Function for calculation of mass center of selected area
    ________________________________________________________
    Arguments:

    wln_sel (float array) - wavelength in selected area
    flx_sel (float array) - flux in selected area
    _____________________________________________
    Returns:

    Mass center of selected area
    """

    mx = np.sum(wln_sel[k] * flx_sel[k] for k in range(nf - ns))
    m = np.sum(flx_sel)
    mc = mx / m

    return mc


def calc_int(wln_sel, flx_sel, cnt_sel):
    """
    Function for calculation area between spectrum and continuum
    in selected area
    ________________
    Arguments:

    wln_sel (float array) - wavelength in selected area
    flx_sel (float array) - flux in selected area
    cnt_sel (float array) - continuum curve in selected area
    ________________________________________________________
    Returns:

    Intensity (area between spectrum and continuum)
    """

    intensity = np.trapz(flx_sel - cnt_sel, wln_sel)

    return intensity


def fit_gauss(wln_sel, flx_sel, cnt_lvl):
    """
    Function to fitting gaussian in selected area
    _____________________________________________
    Arguments:

    wln_sel (float array) - wavelength in selected area
    flx_sel (float array) - flux in selected area
    cnt_lvl (float array) - median continuum level in
                            selected area
    _________
    Returns:

    Coefficients of gauss curve
    """

    # Initial approximation
    amp = np.max(flx_sel) - np.min(flx_sel)
    mean = calc_masc(wln_sel, flx_sel)
    sigma = np.std(flx_sel)

    popt, pcov = curve_fit(
        gauss_function,
        wln_sel,
        flx_sel - cnt_lvl,
        p0=[amp, mean, sigma]
    )

    return popt