'''
Sean Keenan, PhD Physics
Quantum Memories Group, Heriot-Watt University, Edinburgh
2023

Functions designed to perform mathematical operations on data
'''

import numpy as np
from scipy.fftpack import fft, fftfreq

<<<<<<< HEAD
def bin_data(data, N: int = 10, edge: bool = False):
    """
    Bin the data and return mean
=======
<<<<<<< HEAD
def bin_data(data, N: int = 10, edge: bool = False):
    """
    Bin the data and return mean
=======
def bin_data(data, N: int=10):
    """
    Average a list of data or bin the data and return mean
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610
>>>>>>> 1157bed486618d4b97a3c24721a673a05e366e0e
    
    Parameters
    ----------

    data : list of data to average
<<<<<<< HEAD
    bins : number of bins to group data into
    edge : choose to include right or left edge of bin.
=======
<<<<<<< HEAD
    bins : number of bins to group data into
    edge : choose to include right or left edge of bin.
=======
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610
>>>>>>> 1157bed486618d4b97a3c24721a673a05e366e0e

    Returns
    -------

<<<<<<< HEAD
    mean : value of data
    """
    minimum = min(data)
    maximum = max(data)
    bins = np.linspace(minimum, maximum, N+1) 
    binned = np.digitize(data, bins, right=edge)

    return data[binned == np.bincount(binned).argmax()].mean()
=======
<<<<<<< HEAD
    mean : value of data
    """
    minimum = min(data)
    maximum = max(data)
    bins = np.linspace(minimum, maximum, N+1) 
    binned = np.digitize(data, bins, right=edge)

    return data[binned == np.bincount(binned).argmax()].mean()
=======
    x : average or mean value of data
    """
    if N != 0:
        minimum = np.min(data)
        maximum = np.max(data)
        bins = np.linspace(minimum, maximum, N+1) 
        binned = [[x for x in data if x > (bins[i]) and x < (bins[i+1])]
                for i in range(N)]
        
        a, b = find_longest(binned)
        
        mean = sum(a) / b
    else:
        mean = sum(data) * 1/len(data)

    return mean
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610
>>>>>>> 1157bed486618d4b97a3c24721a673a05e366e0e

def find_longest(data_list):
    """
    Find longest list and length within a lst
    
    Parameters
    ----------

    data_list : list of data

    Returns
    -------

    longest : longest list
    length : length of longest list
    """
    longest = max(data_list, key = lambda i: len(i))
    length = max(map(len, data_list))

    return longest, length

def calc_fft(time, amplitude):
    """
    Perform FFT calculation for amplitude component and generate the frequency
    from times.

    Parameters
    ----------
    time : 1D data array / list to use as reference
    amplitude : 1D data array / list of transmission data

    Returns
    -------
    frequencies : list of frequency values from input time data
    ffts : list of fft calculated from input amplitude data

    """
    N = len(time)
    T = time[1] - time[0]
    fftd = fft(amplitude)
    frequencies = fftfreq(N, T)

    return frequencies, fftd

def OD_calc(ref_data, trans_data, c_factor: float=1):
    """
    Perform OD calculation for transmission data and adjust the reference
    using the correction factor if neccesary

    Parameters
    ----------
    reference : data array to use as reference
    transmission : data array of transmission data
    correction : correction factor for the reference data

    Returns
    -------
    calculated optical depth

    """
    return np.log((ref_data * c_factor)/trans_data)

<<<<<<< HEAD
def ODset_calc(reference_sets, transmitted_sets, c_factor: float=1):
=======
def ODset_calc(reference_sets, transmitted_sets, c_factor: float = 1):
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610

    OD_sets = []
    for index in range(len(reference_sets)):
        OD_temp = []
        for reference in reference_sets[index]:
            for transmission in transmitted_sets[index]:
<<<<<<< HEAD
                OD_temp.append(OD_calc(reference, transmission, c_factor))
=======
                OD_temp.append(OD_calc(reference, transmission))
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610
            OD_sets.append(OD_temp)

    return OD_sets

def zoom(data, bounds:tuple=()):
    """
    zoom in on a particular area of interest in a dataset

    Parameters
    ----------
    data : list / array - data to perform zoom
    bounds : tuple - lower and upper bounds of the region of interest

    Returns
    -------
    start, stop : start and stop index for the zoomed data

    """
    start = np.argmin(abs(data - bounds[0]))
    stop = np.argmin(abs(data - bounds[1]))

<<<<<<< HEAD
    return start, stop
=======
<<<<<<< HEAD
    return start, stop
=======
    return start, stop

def data_shift(data, shift):
    """
    Perform a shift for each value in an array of data

    Parameters
    ----------
    data_sets : array like 
    shift : value to shift data by or array like

    Returns
    -------
    shifted : list of shifted data 

    """
    if type(data) == list:
        shifted = [x + shift for x in data]
    else:
        shifted = data + shift
        
    return shifted
>>>>>>> 6451c49e444eebae6b78a23313ff53f9ac92b610
>>>>>>> 1157bed486618d4b97a3c24721a673a05e366e0e
