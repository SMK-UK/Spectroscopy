import numpy as np
from scipy.optimize import curve_fit
import matplotlib as mp

def lorentzian(x, amp, offset, x_0, gamma):
    """
    Generates Lorentzian function with given parameters.

    Parameters
    ----------

    x : array_like
        Input range of frequencies
    amp : single value
        Height of peak
    offset : Single value
        Y offset
    x_0 : single value
        Central frequency of Lorentzian
    gamma : single value
        FWHM of Lorentzian
    
    Returns
    -------

    out : 1-D array
        Output amplitudes as function of x

    """
    return (amp / (1 + (2 * (x - x_0) / gamma) ** 2)) + offset

def fitlorentz(x, height, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to a Lorentzian function
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    height : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Lorentzian function; amp, amp_0, x_0, gamma
    meth : Single string {'lm', 'tf', 'dogbox'}, optional
        Method to use for optimisation. See 
        scipy.optimize.curve_fit for details
    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on parameters. Defaults to 
        no bounds. 
        See scipy.optimize.curve_fit for details

    Returns
    -------

    fit : 1D array
        Fitted variables
    fit_err : 1D array
        Uncertainty in fitted variables
    """
    fit, success = curve_fit(lorentzian, x, height, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def bin_data(y_data, bins):

    bin_size = np.amax(y_data) / bins
    binned_data = []
    binned_size = []
    start = 0
    stop = len(y_data)

    for multiplier in range(bins):
        for value in y_data[start:stop]:
            temp = []
            if value >= (bin_size * multiplier) or value <= ((multiplier + 1) * bin_data):
                temp.append(value)
                start = np.where(value > bin_size * multiplier)
                stop = np.where(bin_size * (multiplier + 1))
            
            binned_data.append(temp)
            binned_size.append(len(binned_data))
            
    return binned_data, binned_size

def check_str(input_string):

    if any(char.isdigit() for char in input_string) == True:

        char_allow = set("0123456789\n\t\r eE-+,.;")
        validation = set((input_string))
        logical = validation.issubset(char_allow)
    else:
        logical = False

    return logical
