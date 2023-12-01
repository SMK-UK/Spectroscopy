'''
Specific functions for handling spectroscopy data and analysing

TO DO:

convert this to a general class
update plotter to take strings in order to change colours

'''
from math import log
import matplotlib.pyplot as mp
from natsort import natsorted, os_sorted
import numpy as np
import os, re
import pandas as pd
from scipy.fftpack import ifft, fft, fftfreq
from scipy.signal import find_peaks, fftconvolve

c = 299792458

# TODO incorporate numpy arrays and conditionals to deal with numpy arrays
# in functions



def bin_data(data: list[float], N: int=10):
    """
    Average a list of data or bin the data and return mean
    
    Parameters
    ----------

    data : list of data to average

    Returns
    -------

    x : average or mean value of data
    """
    if N != 0:
        minimum = min(data)
        maximum = max(data)
        bins = np.linspace(minimum, maximum, N+1) 
        binned = [[x for x in data if x > (bins[i]) and x < (bins[i+1])]
                for i in range(N)]
        
        mean = sum(find_longest(binned)[0]) / find_longest(binned)[1]
    else:
        mean = sum(data) * 1/len(data)

    return mean

def converter(data: list[float]|float, d_type:int=1, 
              c_type:int = 0, scale:float = 1):
    """
    Convert list or single value from wavelength, frequency 
    or wavenumber to another.
    
    Parameters
    ----------

    data : list of lists
    d_type : Input data type
    0: wavenumber
    1: frequency
    2: wavelength
    c_type : Output data type
    0: wavenumber
    1: frequency
    2: wavelength
    scale : scaling factor

    Returns
    -------

    converted : list of converted values
    """
    if type(data) == float or int:
        convert = [data]
    else:
        convert = data
        
    converted = []
    wavelengths = []

    if d_type == 0:
        wavelengths = [1E7 / (value*scale) for value in convert]
    elif d_type == 1:
        wavelengths = [c / (value*scale) for value in convert]
    elif d_type == 2:
        wavelengths = convert

    if c_type == 0:
        converted = [1E7 / (wavelength) for wavelength in wavelengths]
    elif c_type == 1:
        converted = [c / (wavelength) for wavelength in wavelengths]
    elif c_type == 2:
        converted = wavelengths

    if len(converted) == 1:
        converted = converted[0]
    
    return converted

def check_len(data_lists: list[list]):
    """
    Checks nested list for each list lengths and populate a list of lists
    containing the corresponding length
    
    Parameters
    ----------

    lists : list of lists

    Returns
    -------

    boolean : True or False value depending on if the 
    lists are all the same length lengths : list or 
    single value of lengths for each list in lists
    """
    # creat list of all nested list lengths
    data_set_lengths = [len(data_set_child) for data_set in data_lists 
                        for data_set_child in data_set]
    # check set for different lengths and populate a list
    lengths = [x for x in set(data_set_lengths)]
    # if only one length all lengths are the same so boolean is True
    if len(lengths) == 1:
        boolean = True
        indexes = None
    else:
        boolean = False
        indexes = [[len(x) for x in data_set_child] for data_set_child
                    in data_lists]

    return boolean, indexes

def check_str(string_one, string_two):
    """
    Checks string for certain characters and flag if true
    
    Parameters
    ----------

    string_one : string to check
    string_two : string / characters to check against
    flip : choose to flip the strings 

    Returns
    -------

    Boolean
    """
    validation = set(string_one)
    char_allow = set(string_two)
   
    return validation.issubset(char_allow)

def check_digits(input_string: str):
    """
    Checks if a string contains only digits and flag if True
    
    Parameters
    ----------

    input_string : string 

    Returns
    -------

    logical : Boolean
    """
    # check input string for digits and flag True
    if any(char.isdigit() for char in input_string) == True:
        # search input_string for any of the following characters 
        # and spaces / indents
        char_allow = set("0123456789\n\t\r eE-+,.;")
        validation = set((input_string))
        # check if any allowed characters in the input string
        logical = validation.issubset(char_allow)
    else:
        logical = False

    return logical

def data_extract(paths: list[str], keys: list[str]=[], tail: int=1, 
                include: bool=True):
    """
    search a given path or list of paths for strings and extract the data
    from selected files depending on the discriminator (keys)

    Parameters
    ----------

    paths : file paths / path
    keys : list of key values to search for in path if required
    tail : int value 1 or 0 to search head or tail of path
    function : True or False to include the data with key or exclude
    
    Returns
    -------

    extracted_data : list of data read from path
    extracted_metadata : list of metadata read from path
    
    """
    extracted_data = []
    extracted_metadata = []
    if keys:
        for key in keys:
            extracted_data_children = []
            extracted_metadata_children = []
            for path in paths:
                if include == True:
                    # extract data from path if it contains the key
                    if key in os.path.split(path)[tail]:
                        extracted_data_children.append(open_data(path)[0])
                        extracted_metadata_children.append(open_data(path)[1])
                    else:
                        continue
                else:
                    if key in os.path.split(path)[tail]:
                        # extract data from path if it doesn't contain the key
                        extracted_data_children.append(open_data(path)[0])
                        extracted_metadata_children.append(open_data(path)[1])
                    else:
                        continue
            extracted_data.append(extracted_data_children)
            extracted_metadata.append(extracted_metadata_children)
    else:
        for path in paths:
            extracted_data.append(open_data(path)[0])
            extracted_metadata.append(open_data(path)[1])

    return extracted_data, extracted_metadata

def data_fft(time: list[float], amplitude: list[float]):
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

def data_shift(data_sets: list[list[list[int]]], shift: int|float):
    """
    Perform a shift for each value in a list of data

    Parameters
    ----------

    data_sets : 2D data array / list to perform shift on
    shift : value to shift data by

    Returns
    -------

    shifted_sets : list of shifted data 
    """
    return [[[value + shift for value in data_set_child]
                    for data_set_child in data_sets[index]] for 
                    index in range(len(data_sets))]

def df_average(data_frames: list):
    """
    Average a set of data frames and return the averaged
    data frame
    
    Parameters
    ----------

    data_frames : list of data frames to average  

    Returns
    -------

    averaged_data : data frame containing the averaged data from
    data_frames
    """
    summed = 0
    for data_frames_child in data_frames:
        summed += data_frames_child

    return summed / len(data_frames)

def dir_interogate(path: str, extensions: tuple[str,...] = (), 
                   exceptions: tuple[str,...] = (), 
                   folders: tuple[str,...] = ()):
    """
    Interogate directory and extract all folders and files with 
    the specified extensions

    Parameters
    ----------

    path : string - main folder / directory to interrogate
    exts : tuple / list - file extensions to check for in directory
    exceptions : tuple / list - file extensions / strings to exclude
    folders : list - selected folders to extract from

    Returns
    -------

    folder_list : list of folder names
    file_list : list of file names

    """
    folder_list = []
    file_list = []
    for root, dirs, files in natsorted(os.walk(path)):

        if dirs:
            dirs = natsorted(dirs)
            if not folders:
                folder_list = dirs
            else:
                folder_list = [folder for folder in dirs 
                               if folder in folders]
            if exceptions:
                folder_list = [folder for folder in folder_list
                               if not any([x in folder for x in exceptions])]

        if not dirs:
            temp_files = []
            if not folders:
                temp_files = files
            elif any([x in os.path.split(root) for x in folders]):
                temp_files = files
            if exceptions:
                temp_files = [file for file in temp_files
                              if not any([x in file for x in exceptions])]
            if extensions:
                temp_files = [file for file in temp_files
                              if file.endswith(extensions)]
            if temp_files:
                file_list.append(natsorted(temp_files))

    if len(file_list) == 1:
        file_list = [file_name for sublist in file_list
                     for file_name in sublist]
    
    return folder_list, file_list

def excel_extract(folder_names: list[str], file_names: list[list[str]],
                  average: bool=False):
    # TO DO : make this work for spectrscopy data and test the speed compared to text parse
    return [[open_excel(os.path.join(folder, file)) for file in file_names[index]] for index, folder in enumerate(folder_names)]

def find_tau(y: list[float], x: list[float]=[], modifier: float=0.9):
    """
    # TO DO - add functionality for working wih three or more pulses

    Find the difference in time between two pulses and return
    the indexes of these points.

    Uses find_trigger

    Parameters
    ----------

    y : array like
        Pulsed signal
    x : array like
        Time data / data to calculate difference between pulses
    modifier : single value
        Threshold multiplier for trigger (percentage of maximum value of 
        data)
    
    Returns
    -------

    centres : list of int
        Indexes of centres of pulses
    tau     : single value float
        Difference between centres for x data

    """
    indexes = find_trigger(y, modifier, edge='both')
    indexes = np.sort(indexes)
    pulses = len(indexes)//2
    centres = [(indexes[(idx*2)+1] + indexes[idx*2])//2 for idx in range(pulses)]
    if x:
        tau = x[centres[1]] - x[centres[0]]
        return tau, centres
    else:
        return centres
    
def find_trigger(data, modifier: float=0.9, edge: str='rise'):
    """
    Find rising or falling edge of a trigger signal

    Parameters
    ----------

    data : array like
        Trigger signal
    modifier : single value
        Threshold multiplier for trigger (percentage of maximum value of 
        data)
    edge : rise, fall, both
        rise = rising edge
        fall = falling edge
        both = all edges
    
    Returns
    -------

    position : int
        index of trigger point

    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    
    if modifier:
        threshold = np.max(data) * modifier
    else:
        threshold = np.max(data) * 0.9

    sign = data >= threshold
    search = np.round(fftconvolve(sign, [1, -1]))

    if edge == 'rise':
        position = int(np.min(np.where(search == 1)[0]))
    elif edge == 'fall':
        position = int(np.max(np.where(search == -1)[0]))
    else:
        rising = np.where(search == 1)[0]
        falling = np.where(search == -1)[0]
        position = np.append(rising, falling)
        
    return position

def find_numbers(string:str, pattern:str='-?\ *\d+\.?\d*(?:[Ee]\ *-?\ *\d+)?'):
    """
    Checks string for numbers
    
    Parameters
    ----------

    paths : path or list of paths

    Returns
    -------

    numbers : int or list of ints
    """
    # will return combined values i.e. 187 will be returned '187' and not
    #'1', '8', '7'
    match_number = re.compile(pattern)
    numbers = [x for x in re.findall(match_number, string)]

    if len(numbers) == 1:
        numbers = numbers[0]

    return numbers

def find_OD(y_values:list[float], peaks:list[int], lims:tuple=()):
    """
    Find OD of peak data
    
    Parameters
    ----------

    data : list of data to extract OD from
    peaks : list of peak values in data
    N : number of bins 

    Returns
    -------

    OD : OD value at peak
    """

    return [y_values[index] for index in peaks if index >= lims[0] and index <= lims[1]]

def find_longest(data_list: list[list[float]]):
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

def OD_calc(ref_data: list[list[list[list[float]]]], 
            trans_data: list[list[list[list[float]]]],
            correction: bool=True, c_factor: float=1):
    """
    Perform OD calculation for transmission data and adjust the reference
    using the correction factor if neccesary

    Parameters
    ----------

    reference : 2D data array / list to use as reference
    transmission : 2D data array / list of transmission data
    correction : correction factor for the reference data

    Returns
    -------

    x : list of x values from input x data
    y : list of OD calculated from input y data
    """
    x = []
    y = []
    for index in range(len(ref_data)):
        temp_x = []
        temp_y = []
        # perform correction on the reference data and then calculate the OD
        for references in ref_data[index]:
            reference = references[1]
            if correction == True:
                reference = [x*c_factor for x in reference]
            for transmission in trans_data[index]:
                temp_x.append(transmission[0])
                temp_y.append([log(a / b) for a, b 
                               in zip(reference, transmission[1])])
            x.append(temp_x)
            y.append(temp_y)

    return x, y

def open_data(path: str):
    """
    Open a given file and read the first two columns to a list. Works with
    columns of different length

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    data_list : list of data read from path
    metadata_list : list of metadata read from path
    
    """
    data_list = 0
    metadata_list = 0
    with open(path, 'r', newline='') as raw_file:
    # cycle through each row in the file
        for row in raw_file:
            # check row for specific string / values
            if check_digits(row) == True:
                # generate list to populate with column data
                data_temp = [i for i in re.split(r"[\t|,|;]", row)
                             if i != '' and i != '\r\n']
                if not data_list:
                    data_list = [[] for _ in range(len(data_temp))]
                for index, data in enumerate(data_temp):
                    if len(data_list) < index + 1:
                        data_list.append([])
                    data_list[index].append((float(data)))
            else:
                # extract metadata
                metadata_temp = [i for i in re.split(r"[\t|,|;]", row)
                                 if i != '' and i != '\r\n']
                if not metadata_list:
                    # generate list to populate with column metadata
                    metadata_list = [[] for _ in range(len(metadata_temp))]
                for index, metadata in enumerate(metadata_temp):
                    if len(metadata_list) < index + 1:
                        metadata_list.append([])
                    metadata_list[index].append(metadata)
        raw_file.close()

    return data_list, metadata_list

def excel_to_numpy(path: str, seperators: str=','):
    """
    Open a given excel / csv file and generate list

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    excel_data : list of column data from pandas data frame
    
    """
    temp_df = pd.read_csv(path, sep=seperators)
    excel_data = [temp_df[x].to_numpy() for x in temp_df]

    if len(excel_data) == 1:
        excel_data = [value for sublist in excel_data for value in sublist]

    return excel_data

>>>>>>> functions
def open_excel(path: str, seperators: str=','):
    """
    Open a given excel / csv file and generate list

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    excel_data : list of column data from pandas data frame
    
    """
    temp_df = pd.read_csv(path, sep=seperators)
<<<<<<< HEAD
    excel_data = [temp_df[x].values.tolist() for x in temp_df]
=======
    excel_data = [temp_df[x].tolist() for x in temp_df]
>>>>>>> functions

    if len(excel_data) == 1:
        excel_data = [value for sublist in excel_data for value in sublist]

    return excel_data

def open_text(path: str):
    """
    Open a given file and read the first two columns to a list. Works with
    columns of different length

    Parameters
    ----------
    path : file path
    
    Returns
    -------
    data_list : list of data read from path
    metadata_list : list of metadata read from path
    
    """
    data_list = []
    with open(path, 'r', newline='') as raw_file:
    # cycle through each row in the file
        for row in raw_file:
            # generate list to populate with column data
            data_temp = [i for i in re.split(r"[\t|,|;]", row)
                            if i != '' and i != '\r\n']
            if not data_list:
                data_list = [[] for _ in range(len(data_temp))]
            for index, data in enumerate(data_temp):
                if len(data_list) < index + 1:
                    data_list.append([])
                data_list[index].append(data)
        raw_file.close()

        if len(data_list) == 1:
            data_list = [data for sublist in data_list for data in sublist]

    return data_list
<<<<<<< HEAD
   
=======

>>>>>>> functions
def peak_find(x_data_sets: list[list[list[int|float]]], 
              y_data_sets: list[list[list[int|float]]], 
              prom_tol=None, top_tol=None, lims=None):
    """
    Find peaks in data

    Parameters
    ----------

    data_sets : 2D data array / list to perform shift on
    args : peak finding conditions (see scipy.signal.find_peaks)

    Returns
    -------

    peaks_data : indexes of peaks for each data set
    """  
    peaks_data = []
    lower = 0
    upper = -1
    prom = prom_tol
    top = top_tol

    for index in range(len(y_data_sets)):
        temp = []
        for x_data_sets_child, y_data_sets_child in zip(x_data_sets[index], 
                                                        y_data_sets[index]):
            if lims:              
                lower, upper = zoom(x_data_sets_child, lims)
            data_max = max(y_data_sets_child[lower:upper])
            if prom_tol:
                prom = prom_tol * data_max
            if top_tol:
                top = top_tol * data_max
            peaks, _ = find_peaks(y_data_sets_child[lower:upper], 
                                  height=top, prominence=prom)
            temp.append([peak + lower for peak in peaks])
        peaks_data.append(temp)

    return peaks_data

def peak_freq(peaks_parent:list[list[list[float]]],
              wavelength_parent:list[list[list[float]]],
              lims=None):
    """
    convert a series of wavelength values to frequency 
    based on given list of indexes

    Parameters
    ----------

    peaks_parent : list / array containing index of wavelength
    values to convert
    lims : list|tuple - lower and upper bounds of interest wavelengths

    Returns
    -------

    frequencies : list of frequency values

    TO DO: superfluous - use converter and change this to extract
    x value for peaks
    """
    
    frequencies = []

    for m, peaks_child in enumerate(peaks_parent):
        frequency_subset = []
        for n, peak_subset in enumerate(peaks_child):
            if lims:
                lower, upper = zoom(wavelength_parent[m][n], lims)
            else:
                lower = 0
                upper = len(wavelength_parent[m][n])
            frequency_subset.append([c * 1 / wavelength_parent[m][n][i] for i in peak_subset if i >= lower and i <= upper])
        frequencies.append(frequency_subset)

    if len(frequencies) == 1:
        frequencies = [frequency for sublist in frequencies for frequency in sublist]
        
    return frequencies

def plotter(x_data, y_data, data_indexes=[], keys:list=[], shifter: int|float=0,
            axis_lbls=None, sec_axis=True, save=False, 
            data_labels=[], lims:tuple=(), woi:list=[], res=80):
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
    data_lbl = None
    lower = 0
    upper = -1
    if not keys:
        keys = []

    for m, key in enumerate(keys):
        fig, ax = mp.subplots()
        ax.grid(True, color='silver', linewidth=0.5)
        if axis_lbls:
            ax.set_title('Halfwave Plate: ' + key)
            ax.set(xlabel=axis_lbls[0], ylabel=axis_lbls[1])
        if sec_axis:
            sec_ax = ax.secondary_xaxis('top', functions=
                                        (lambda x: 1e7/x, lambda x: 1e7/x))
            sec_ax.set_xlabel('Wavelength (nm)')
        if woi:
            for woi_set in woi:
                for vline in woi_set[0]:
                    ax.axvline(x=vline, linestyle=woi_set[1], color=woi_set[2], linewidth='2')

        shift = 0
        for o, x in enumerate(x_data[m]):
            x = np.array(x)
            y = np.array([value + shift for value in y_data[m][o]])
            plot_colour = mp.cm.winter(np.linspace(0, 1, len(x_data[m])))
            if lims:
                lower, upper = zoom(x, lims)
            if data_labels:
                data_lbl = os.path.split(data_labels[o])[1]
            ax.plot(x[lower:upper], y[lower:upper], color=plot_colour[o],
                    linestyle='-', linewidth=0.8, alpha=1, label=data_lbl)
            if data_indexes:
                data_index = np.array([i for i in data_indexes[m][o]
                            if i >= lower and i <= upper])
                if data_index.size > 0:
                    ax.plot(x[data_index], y[data_index], marker='x',
                            color=plot_colour[o], linestyle='None', alpha=1,
                            label='_nolegend_')
            shift += shifter

        ax.legend(loc='best', fontsize=8)
        fig.tight_layout()

        if save:
            folder = os.path.split(data_labels[0])[0]
            region = str(round(x[lower])) + '_' + str(round(x[upper])) \
            + '_' + key
            name = os.path.join(folder, region + '.png')

            fig.savefig(fname=name, dpi=res, format='png', bbox_inches='tight')
    
def read_files(folder_list, file_list):
    # TO DO - deprecated as of latest update - check occoruences and remove.
    # Replace with new search_paths functionality
    """
    Create file path in a folder for parsing data in the file

    Parameters
    ----------

    folder_list : list of folder names
    file_list : list of file names

    Returns
    -------

    path : file path name
    """
    path = []
    for index, folder in enumerate(folder_list):
        files = []
        for file in file_list[index]:
            files.append(os.path.join(folder, file))
        
        path.append(files)

    return path
    
def search_paths(paths: list, keys: tuple[str,...]):
    """
    Search paths for keys and then extract the file pathnames

    Parameters
    ----------

    paths : paths to search
    keys : key strings to look for in path name

    Returns
    -------

    key_paths : list of requested path names
    excluded_paths : list of other path names
    """
    key_paths = []
    excluded_paths = []
    for path in paths:
        if any([x in path for x in keys]):
            key_paths.append(path)
        else:
            excluded_paths.append(path)

    return key_paths, excluded_paths

def stdev(data:list, N: int=10):
    """
    return the variance of a population set
    
    Parameters
    ----------

    data : list of data to calculate variance

    Returns
    -------

    variance : variance of data
    """
    mean = bin_data(data, N)

    return np.sqrt(sum([(mean - x)**2 for x in data]) * 1/len(data))

def zero_data(data:list[float]):
    """
    subtract minimum value (negative) from a data set to shift all 
    values above zero

    Parameters
    ----------

    data : list / array - data to perform shift

    Returns
    -------

    data with values shifted by the minimum value
    """
    minimum = min(data)

    return [value - minimum for value in data]

def zoom(data:list[float], bounds:tuple=()):
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

    # TO DO - make into generic index finder
    start = np.argmin(np.abs(np.asarray(data) - bounds[0]))
    stop = np.argmin(np.abs(np.asarray(data) - bounds[1]))

    return start, stop