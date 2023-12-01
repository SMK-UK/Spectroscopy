'''
Generic fitting functions 
'''

from math_funcs import zoom
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

def dbl_exp_decay(x, y_1, y_2, T1, T2, offset):
    """
    Generates approximate T1 decay with given parameters
    
    Parameters
    ----------

    x : 1D array 
        Positional arguments for gaussian
    y_0 : Single value
        Y intercept / start of decay profile
    T1 : Single value
        T1 lifetime of excited state
    T2 : Single value
        Additional dephasing term of excited state
    off : single value
        Offset of the data

    Returns
    -------

    1D array of height values for the positional arguments given in x
    """

    return (y_1 * np.exp(-x/T1)) + (y_2 * np.exp(-x/T2)) + offset

def exp_decay(x, y_0, T1, offset):
    """
    Generates approximate T1 decay with given parameters
    
    Parameters
    ----------

    x : 1D array 
        Positional arguments for gaussian
    y_0 : Single value
        Y intercept / start of decay profile
    T1 : Single value
        T1 lifetime of excited state
    off : single value
        Offset of the data

    Returns
    -------

    1D array of height values for the positional arguments given in x
    """

    return (y_0 * np.exp(-x/T1)) + offset

def fit_dbl_exp_decay(x, y, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to an approximate double exponetial decay curve
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    y : 1D array
        y values corresponding to x values
    params : 1D array, optional
        Guess values for T1 decay; y_0, T1
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
    fit, success = curve_fit(dbl_exp_decay, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def fit_exp_decay(x, y, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits data to an approximate T1 decay curve
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    y : 1D array
        y values corresponding to x values
    params : 1D array, optional
        Guess values for T1 decay; y_0, T1
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
    fit, success = curve_fit(exp_decay, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def fit_gauss(x, amp, params=None, meth=None, lims:tuple=(-np.inf, np.inf)):
    """
    Fits a gaussian function to the data

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
            
def fit_gls(x, amp:float, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits a Voigt profile to the data using the GLS method
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    amp : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Voigt profile; y_0, amp_g, x_0g, sigma, amp_l, x_0l, gamma, eta
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

def fit_lorentz(x, y, params=None, meth=None, lims:tuple=(-np.inf, np.inf)):
    """
    Fits a Lorentzian function to the data
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    y : 1D array
        Amplitude values corresponding to x values
    params : 1D array, optional
        Guess values for Lorentzian function; amp_0, x_0, gamma
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
    fit, success = curve_fit(lorentzian, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def fit_Ngauss(x, y, params=None, meth=None, lims:tuple=(-np.inf, np.inf)):
    """
    Fits N number of Gaussian to the data
    
    Parameters
    ----------

    x : 1D array 
        x values of orginal data
    y : 1D array
        y values corresponding to x values
    params : 1D array, optional
        Guess values for gaussians in list: amp, y_0, x_0, sigma
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
    fit, success = curve_fit(N_gaussian, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def fit_straight(x, y, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits a straight line function to the data to 
    
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

def gaussian(x, amp:float, y_0:float, x_0:float, sigma:float):
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

def rise_time(t, amp, t_0, t_r):
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
    return amp * (1 - np.exp(-(t-t_0)/t_r))

def fit_rise_time(x, y, params=None, meth=None, lims=(-np.inf, np.inf)):
    """
    Fits a straight line function to the data to 
    
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
    fit, success = curve_fit(rise_time, x, y, p0=params, method=meth, bounds=lims)
    fit_err = np.sqrt(np.diag(success))

    return fit, fit_err

def lorentzian(x, amp:float, y_0:float, x_0:float, gamma:float):
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

def N_gaussian(x, *params):
    """
    Generates sum of N Gaussians with given parameters
    
    Parameters
    ----------

    x : 1D array 
        Positional arguments for Gaussian
        
    params : list of values containing (in order) 

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
    assert len(params) % 4 == 0, 'params must be a multiple of 4'
    y = np.zeros_like(x)
    for i in range(0, len(params), 4):
        y = y + gaussian(x, params[i], params[i+1], params[i+2], params[i+3])

    return y

def peak_find(y, x=None, prom_tol=None, top_tol=None, lims=None):
    """
    Find peaks in data

    Parameters
    ----------

    y : array to find peaks
    x : corresponding
    args : peak finding conditions (see scipy.signal.find_peaks)

    Returns
    -------

    peaks_data : indexes of peaks for each data set

    """
    lower = 0
    upper = -1

    if lims:
        lower, upper = zoom(x, bounds=lims)  

    data_max = np.max(y[lower:upper])

    if prom_tol:
        prom_tol *= data_max
    if top_tol:
        top_tol *= data_max

    peaks, _ = find_peaks(y[lower:upper], height=top_tol, prominence=prom_tol)
    
    return peaks

def pseudo_voigt(x:list[float], y_0:float, amp_g:float, x_0g:float,
                sigma:float, amp_l:float, x_0l:float, gamma:float, eta:float):
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
    pv = (eta * amp_g * (np.exp(-((x - x_0g) ** 2) / (2 * sigma ** 2)))) + ((1-eta)
        * amp_l * ((0.5*gamma)**2/((x-x_0l)**2 + (0.5*gamma)**2))) + y_0

    return pv

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
    return a*x + b