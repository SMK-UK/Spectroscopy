from cmath import isfinite
import numpy as np
from scipy.optimize import curve_fit
import matplotlib as mp
from scipy.special import wofz

def check_str(input_string):
    """
    Checks string for certain characters
    
    Parameters
    ----------

    input_string : string 

    Returns
    -------

    logical : Boolean
        True or False  
    """
    if any(char.isdigit() for char in input_string) == True:
        # search input_string for any of the following characters
        char_allow = set("0123456789\n\t\r eE-+,.;")
        validation = set((input_string))
        logical = validation.issubset(char_allow)
    else:
        logical = False

    return logical

def check_len(lists):
    """
    Checks nested list for each list lengths
    
    Parameters
    ----------

    lists : list of lists

    Returns
    -------

    boolean : True or False value depending on if the lists are all the same length
    lengths : list or single value of lengths for each list in lists
        True or False  
    """
    check = [len(data) for group in lists for data in group]
    lengths = [x for x in set(check)]
    # if only one length all lengths are the same so boolean is True
    if len(lengths) == 1:
        boolean = True
        indexes = None
    else:
        boolean = False
        indexes = [[index_1, index_2] for index_1, value_1 in enumerate(lists) for index_2, value_2 in enumerate(value_1) if len(value_2) > min(lengths)]
    
    return boolean, indexes
    
def straight(x, a, b):
    """
    Generates straight line function with given parameters.

    Parameters
    ----------

    x : array_like
        Input range of x values
    a : single value
        gradient or slope of line
    b : single value
        Y-interecept value
    
    Returns
    -------

    out : 1-D array
        y values as a function of x

    """
    return (a*x + b)

def fitstraight(x, y, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to a straight line function
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    y : 1D array
        y values corresponding to x values
    params : 1D array, optional
        Guess values for straight line; a, b
    meth : Single string {'lm', 'trf', 'dogbox'}, optional
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

    fit, success = curve_fit(straight, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def gaussian(x, amp, y_0, x_0, sigma):
    """
    Generates Gaussian with given parameters
    
    Parameters
    ----------

    x : 1D array 
        Positional arguments for gaussian
    amp : Single value
        Maximum value of gaussian
    y_0 : Single value
        Y Offset
    x_0 : Single value
        Centre of Gaussian peak
    sigma : Single value
        Standard deviation of Gaussian

    Returns
    -------

    1D array of height values for the positional arguments given in x
    """
    return amp * np.exp(-((x - x_0) ** 2) / (2 * sigma ** 2)) + y_0

def fitgauss(x, amp, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Returns seperate x-y Gaussian parameters from fit to 2D gaussian data
    (height, centre_x, width_x, centre_y, width_y)

    Calls to moments(data) in order to extract relevant parameters of the 
    2D gaussian data before finding the fit to the data. See scipy.optimize.curve_fit
    for more on data fitting.

    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    amp : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Lorentzian function; amp, amp_0, x_0, gamma
    meth : Single string {'lm', 'trf', 'dogbox'}, optional
        Method to use for optimisation. See 
        scipy.optimize.curve_fit for details
    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on parameters. Defaults to 
        no bounds. 
        See scipy.optimize.curve_fit for details

    Returns
    -------

    fit_data : 1D Array
        Fitted variables: height, sigma, mean
    fit_err : 1D Array
        Uncertainty in fitted variables
    """
    fit, success = curve_fit(gaussian, x, amp, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def lorentzian(x, amp, y_0, x_0, gamma):
    """
    Generates Lorentzian function with given parameters.

    Parameters
    ----------

    x : array_like
        Input range of frequencies
    amp : single value
        Height of peak
    y_0 : Single value
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
    return (amp * ((0.5*gamma)**2/((x-x_0)**2 + (0.5*gamma)**2))) + y_0
            
def fitlorentz(x, amp, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to a Lorentzian function
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    amp : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Lorentzian function; amp, amp_0, x_0, gamma
    meth : Single string {'lm', 'trf', 'dogbox'}, optional
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
    fit, success = curve_fit(lorentzian, x, amp, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def pseudo_voigt(x, y_0, amp_g, x_0g, sigma, amp_l, x_0l, gamma, eta):
    """
    Generates Pseudo Voigt profile with given parameters using GLS method.

    Parameters
    ----------

    x : array_like
        Input range of frequencies
    y_0 : single value
        Profile Y offset
    amp_g : single value
        Amplitude of Gaussian component
    x_0g : single value
        Central frequency of Gaussian
    sigma : single value
        Standard deviation of Gaussian
    amp_l : single value
        Amplitude of Lorentzian component
    x_0l : single value
        Central frequency of Lorentzian
    Gamma : 
        FWHM of Lorentzian
    Eta : Single Value
        Weighting factor of Gaussian to Lorentzian

    Returns
    -------

    out : 1-D array
        Output amplitudes as function of x

    """
    return (eta * amp_g * (np.exp(-((x - x_0g) ** 2) / (2 * sigma ** 2)))) + ((1-eta) * amp_l * ((0.5*gamma)**2/((x-x_0l)**2 + (0.5*gamma)**2))) + y_0

def fitgls(x, amp, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to a Voigt profile using the GLS method
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    amp : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Voigt profile; I, y_0, x_0g, sigma, x_0l, gamma, eta
    meth : Single string {'lm', 'trf', 'dogbox'}, optional
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
    fit, success = curve_fit(pseudo_voigt, x, amp, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err