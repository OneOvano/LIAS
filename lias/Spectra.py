import numpy as np
import pandas as pd
from urllib.parse import urlencode


def _load(ion, low_w, upp_w, allowed_out=1, forbid_out=1):
    """
    Parser for downloading atomic data from NIST server
    ---------------------------------------------------
    ion - key from Atomic_Data (element and ionisation degree)
    low_v and upp_v - limits of wavelength range (define automatically as the
                                       consequences range of Object_Spectrum)
    """

    nist_db_url = 'http://physics.nist.gov/cgi-bin/ASD/lines1.pl?'
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

    url = nist_db_url + urlencode(settings)

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
    df['Wavelength, Å'] = [np.float(line.replace(" ", ""))
                           for line in df['Wavelength, Å']]
    atomic_data = df
    return atomic_data


class Spectra:
    """
    Loading of object spectrum and atomic data from NIST database
    -------------------------------------------------------------  
    Object_Spectrum - path to file with object spectrum (array with two columns)
    Atomic_Data - keys to atomic spectrum - element and ionization degree
    (e.g. 'He II', all available values you can see on NIST website)
    """

    def describe(self):
        """
        Description with spectrum characteristic
        ----------------------------------------
        Spectral range - minimal and maximal wavelength
        Wavelength step Δλ
        Spectral resolution by formula R = <λ>/Δλ
        Mean continuum level as a median averaging
        """
        
        wln_min = self.Object_Spectrum[0, 0]
        wln_max = self.Object_Spectrum[-1, 0]
        wln_step = (wln_max - wln_min)/len(self.Object_Spectrum[:, 0])
        resole = 0.5*(wln_min + wln_max)/wln_step
        cont = np.median(self.Object_Spectrum[:, 1])
        print(
            """
            \tSpectrum description:
            Minimal wavelength:\t{:.4f} Å 
            Maximal wavelength:\t{:.4f} Å 
            Wavelength step:\t{:.4f} Å
            Average resolution:\t{:.4f}
            Median flux level:\t{:.4e}
            """.format(wln_min, wln_max, wln_step, resole, cont)
        )
    
    def print_NIST(self):
        """
        Print table with lines in console
        """
        
        print(self.Atomic_Data)
        
    def __str__(self):
        print(self.Object_Spectrum)
    
    def __init__(self, Object_Spectrum, Atomic_Data):
        self.ion = Atomic_Data
        self.Object_Spectrum = np.array(Object_Spectrum)
        low_w = self.Object_Spectrum[0, 0]
        upp_w = self.Object_Spectrum[-1, 0]
        self.Atomic_Data = _load(self.ion, low_w, upp_w)