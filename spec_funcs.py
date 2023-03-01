'''
Specific functions for handling spectroscopy data and analysing
'''

import os, re
from math import log
import matplotlib.pyplot as mp
from natsort import natsorted

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

def find_polarisations(paths, tail=1):
    """
    Checks string tail for numbers
    
    Parameters
    ----------

    paths : path or list of paths

    Returns
    -------

    polarisations : int or list of ints
    """
    polarisations = []
    for path in paths:
        polarisations.append(re.findall('\d+', os.path.split(path)[tail])[0])
    
    return polarisations


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

def zoom(data, bounds):
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
    for index, value in enumerate(data):
        if value <= bounds[0]:
            start = index
        if value <= bounds[1]:
            stop = index

    return start, stop

def plotter(x_data, y_data, keys, shifter=0, axis_lbls=None, sec_axis=True, save=False, data_labels=None, lims=None, woi=None):

    try:
        data_lbl = os.path.split(data_labels)[1]
    except:
        data_lbl = None

    for m, key in enumerate(keys):
        fig, ax = mp.subplots(figsize=(8, 5))
        ax.grid(True, color='silver', linewidth=0.5)
        if axis_lbls != None:
            ax.set_title('Halfwave Plate: ' + key)
            ax.set(xlabel=axis_lbls[0], ylabel=axis_lbls[1])
        if sec_axis == True:
            sec_ax = ax.secondary_xaxis('top', functions= (lambda x: 1e7 / x, lambda x: 1e7 / x))
            sec_ax.set_xlabel('Wavenumber (cm$^{-1}$)')
        if woi != None:
            for  vline in woi:
                ax.axvline(x=vline, linestyle='-.')

            
        shift = 0
        for n, x in enumerate(x_data[m]):
            y = [value + shift for value in y_data[m][n]]
            if lims == None:
                lower = 0
                upper = -1
            else:
                lower, upper = zoom(x, lims)
            if data_lbl != None:
                ax.legend(loc='best', fontsize=8)
            ax.plot(x[lower:upper], y[lower:upper], color=None, marker=None, linestyle='-', linewidth=0.8, alpha=1, label=data_lbl)
            shift += shifter

        if save == True:
            folder = os.path.split(data_labels[0])[0]
            region = str(round(x[lower])) + '_' + str(round(x[upper])) + '_' + key
            name = folder + '\\' + region + '.pdf'

            fig.savefig(fname=name, dpi=1200, format='pdf', bbox_inches='tight')
    
def dir_interogate(path, extensions, exceptions):
    """
    Interogate directory and extract all folders
    and files with specified extensions

    Parameters
    ----------

    path : string - main folder / directory to interrogate
    exts : tuple - file extensions to check for in directory
    exceptions : tuple - file extensions / strings to exclude

    Returns
    -------

    folder_list : list of folder names
    file_list : list of file names

    """
    folder_list = []
    file_list = []
    # holder removes first folder from lists so only actual data is used
    holder = 0
    # walk through directory and extract all relevant files
    for root, dirs, files in natsorted(os.walk(path)):
        if holder == 1:
            if any([x in root for x in exceptions]):
                continue
            else:
                folder_list.append(root)
            temp = []
            for file in files:
                if(file.endswith(extensions)):
                    # ignore collection data notes
                    if any([x in file for x in exceptions]):
                        continue
                    else:
                        temp.append(file)
            file_list.append(temp)
        else:
            holder = 1

    return folder_list, file_list

def read_files(folder_list, file_list):
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
        for file in file_list[index]:
            path.append(os.path.join(folder, file))
    
    return path

def open_data(path):
    """
    Open a given file and read the first two columns to a list

    Parameters
    ----------

    path : file path
    
    Returns
    -------

    data : list of data read from path
    
    """
    x = []
    y =[]
    with open(path, 'r', newline='') as raw_file:
        for row in raw_file:
            if check_str(row) == True:
                temp = re.split('\t|,|;', row)
                x.append(float(temp[0]))
                y.append(float(temp[1]))
        raw_file.close()

    return [x, y]

def data_extract(paths, keys, tail=1, include=True):
    """
    search a given path or list of paths for strings and extra the data from selected files 
    depending on the discriminator

    Parameters
    ----------

    path : file path
    keys : list of key values to search for in path
    tail : int value 1 or 0 to search head or tail of path
    function : True or False to include the data with key or exclude
    
    Returns
    -------

    data : list of data read from path
    
    """
    data = []
    for key in keys:
        key_data = []
        for path in paths:
            if include == True:
                if key in os.path.split(path)[tail]:
                    key_data.append(open_data(path))
                else:
                    continue
            else:
                if key in os.path.split(path)[tail]:
                    key_data.append(open_data(path))
                else:
                    continue
        data.append(key_data)    
                    
    return data

def search_paths(paths, keys):
    """
    Search paths for keys and then extract the file pathnames

    Parameters
    ----------

    paths : paths to search
    keys : key strings to look for in path name

    Returns
    -------

    key_paths : list of requested path names

    """
    key_paths = []
    excluded_paths = []
    for path in paths:
        if any([x in path for x in keys]):
            key_paths.append(path)
        else:
            excluded_paths.append(path)

    return key_paths, excluded_paths
    
def OD_calc(ref_data, trans_data, correction=True, c_factor=1):
    """
    Perform OD calculation for transmission data and adjust the reference using correction if neccesary

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
        for references in ref_data[index]:
            if correction == True:
                reference = [x*c_factor for x in references[1]]
            for transmission in trans_data[index]:
                temp_x.append(transmission[0])
                temp_y.append([log(a / b) for a, b in zip(reference, transmission[1])])
            x.append(temp_x)
            y.append(temp_y)

    return x, y
